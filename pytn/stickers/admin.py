from django.contrib import admin

from .models import Sticker, StickerVote


admin.site.register(Sticker)
admin.site.register(StickerVote)
