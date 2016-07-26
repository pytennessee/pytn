from django.conf import settings
from django.conf.urls.defaults import *
from django.conf.urls.static import static

from django.views.generic.simple import direct_to_template

from django.contrib import admin
admin.autodiscover()

import symposion.views
import stickers.views

# from pinax.apps.account.openid_consumer import PinaxConsumer

WIKI_SLUG = r"(([\w-]{2,})(/[\w-]{2,})*)"

urlpatterns = patterns("",
    url(r"^$", direct_to_template, {
        "template": "homepage.html",
    }, name="home"),
    url("^.well-known/acme-challenge/qokKA17AkF2wYWV_Rq6BBDLDEM2mRNu5oCE27caPjko", stickers.views.lets_encrypt, name="lets_encrypt"),
    url(r"^admin/", include(admin.site.urls)),

    url(r"^account/signup/$", symposion.views.SignupView.as_view(), name="account_signup"),
    url(r"^account/login/$", symposion.views.LoginView.as_view(), name="account_login"),
    url(r"^account/", include("account.urls")),

    url(r"^dashboard/", symposion.views.dashboard, name="dashboard"),
    url(r"^speaker/", include("symposion.speakers.urls")),
    url(r"^proposals/", include("symposion.proposals.urls")),
    url(r"^sponsors/", include("symposion.sponsorship.urls")),
    url(r"^boxes/", include("symposion.boxes.urls")),
    url(r"^teams/", include("symposion.teams.urls")),
    url(r"^reviews/", include("symposion.reviews.urls")),
    url(r"^schedule/", include("symposion.schedule.urls")),
    url(r"^markitup/", include("markitup.urls")),
    url(r"^stickers/", include("pytn.stickers.urls")),
    url(r"^api/", include("pytn.api.urls")),

    url(r"^", include("symposion.cms.urls")),
)


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
