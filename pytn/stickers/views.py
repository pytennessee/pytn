from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext

from .models import Sticker, StickerVote
from .forms import StickerForm


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

def lets_encrypt(request):
    return HttpResponse("BRKuJ0viSCzrrPoSYAdOiZ326HIMYJndzZ3deaH1cgM.b6m5qKJTFMPZgBdDHWv1cU_zUprSrr15yWJ_CKofr0o")
