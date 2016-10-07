import logging

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext

from .models import Sticker, StickerVote
from .forms import StickerForm


logger = logging.getLogger(__name__)


@login_required
def sticker_submit(request):
    if request.method == "POST":
        form = StickerForm(request.POST, request.FILES)
        if form.is_valid():
            sticker = form.save()
            sticker.speaker = request.user
            sticker.save()
            return redirect("sticker_review")
    else:
        form = StickerForm()

    return render_to_response("stickers/submit.html", {
        "form": form,
    }, context_instance=RequestContext(request))


@login_required
def sticker_detail(request, pk):
    sticker = get_object_or_404(Sticker, pk=pk)

    return render_to_response("stickers/detail.html", {
        "sticker": sticker,
    }, context_instance=RequestContext(request))


@login_required
def sticker_vote(request, pk):
    sticker = get_object_or_404(Sticker, pk=pk)
    stickervote, created = StickerVote.objects.get_or_create(sticker=sticker, user=request.user)
    return redirect("sticker_review")


@login_required
def sticker_review(request):
    stickers = Sticker.objects.all()

    return render_to_response("stickers/review.html", {
        "stickers": stickers,
    }, context_instance=RequestContext(request))


def find_key(token):
    if token == os.environ.get("ACME_TOKEN"):
        return os.environ.get("ACME_KEY")
    for k, v in os.environ.items():  #  os.environ.iteritems() in Python 2
        if v == token and k.startswith("ACME_TOKEN_"):
            logger.error("Found Token %s", k)
            n = k.replace("ACME_TOKEN_", "")
            return os.environ.get("ACME_KEY_{}".format(n))  # os.environ.get("ACME_KEY_%s" % n) in Python 2


def lets_encrypt(request, token):
#    logger.error("looking for token")
#    key = find_key(token)
#    logger.error('Key %s', key)
    return HttpResponse(str(key))
