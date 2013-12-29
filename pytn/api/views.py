import datetime
import json
from django.core.urlresolvers import reverse
from django.http import HttpResponse

from django.contrib.auth.decorators import login_required
from django.contrib.sites.models import Site

from symposion.schedule.models import Slot


def start_datetime(slot):
    return datetime.datetime(
        slot.day.date.year,
        slot.day.date.month,
        slot.day.date.day,
        slot.start.hour,
        slot.start.minute)


def end_datetime(slot):
    return datetime.datetime(
        slot.day.date.year,
        slot.day.date.month,
        slot.day.date.day,
        slot.end.hour,
        slot.end.minute)


def length_in_minutes(slot):
    return int(
        (end_datetime(slot) - start_datetime(slot)).total_seconds() / 60)


def schedule_json(request):
    everything = bool(request.GET.get('everything'))
    slots = Slot.objects.all().order_by("start")
    
    # request.META['SERVER_PROTOCOL'] # 'HTTP/1.1'
    # protocol = request.META['SERVER_PROTOCOL'].split('/')[0]
    
    # Heroku will add a header to the request to let you know if it's originating from HTTP or HTTPs.
    # https://devcenter.heroku.com/articles/http-routing#heroku-headers
    # X-Forwarded-Proto: the originating protocol of the HTTP request (example: https)
    
    # https://discussion.heroku.com/t/gunicorn-not-setting-wsgi-url-scheme-properly/70
    
    protocol = request.META['wsgi.url_scheme'] # http

    data = []
    for slot in slots:
        if slot.content:
            slot_data = {
                "name": slot.content.title,
                "room": ", ".join(room["name"] for room in slot.rooms.values()),
                "start": start_datetime(slot).isoformat(),
                "end": end_datetime(slot).isoformat(),
                "duration": length_in_minutes(slot),
                "authors": [s.name for s in slot.content.speakers()],
                "released": slot.content.proposal.recording_release,
                # You may wish to change this...
                "license": "All Rights Reserved",
                "contact":
                [s.email for s in slot.content.speakers()]
                if request.user.is_staff
                else ["redacted"],
                "abstract": slot.content.abstract.raw,
                "description": slot.content.description.raw,
                "conf_key": slot.content.pk,
                "conf_url": "%s://%s%s" % (
                    protocol,
                    Site.objects.get_current().domain,
                    reverse("schedule_presentation_detail", args=[slot.content.pk])
                ),
                "kind": slot.kind.label,
                "tags": "",
            }
        elif everything:
            slot_data = {
                "room": ", ".join(room["name"] for room in slot.rooms.values()),
                "start": start_datetime(slot).isoformat(),
                "end": end_datetime(slot).isoformat(),
                "duration": length_in_minutes(slot),
                "kind": slot.kind.label,
                "title": slot.content_override.raw,
            }
        else:
            continue
        data.append(slot_data)

    return HttpResponse(
        json.dumps({'schedule': data}),
        content_type="application/json"
    )
