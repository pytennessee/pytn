import datetime

from django.db import models
from django.contrib.auth.models import User


class Sticker(models.Model):

    title = models.CharField(max_length=100)
    description = models.TextField(
        "Brief Description",
        max_length=400,  # @@@ need to enforce 400 in UI
        help_text="Describe your inspiration for the sticker"
    )
    submitted = models.DateTimeField(
        default=datetime.datetime.now,
        editable=False,
    )
    speaker = models.ForeignKey(User, related_name="stickers", null=True)
    upload = models.FileField("file", blank=True, upload_to="sticker_files")

    #class Meta:
        #ordering = ['-votes']

    def __unicode__(self):
        return self.title


class StickerVote(models.Model):
    sticker = models.ForeignKey(Sticker, related_name="votes")
    user = models.OneToOneField(User)

    def __unicode__(self):
        return '-'.join(['Vote', self.sticker.title])
