import datetime
import os
import uuid

from django.contrib.auth.models import User
from django.db import models


def find_key(token):
    if token == os.environ.get("ACME_TOKEN"):
        return os.environ.get("ACME_KEY")
    for k, v in os.environ.items():  #  os.environ.iteritems() in Python 2
        if v == token and k.startswith("ACME_TOKEN_"):
            n = k.replace("ACME_TOKEN_", "")
            return os.environ.get("ACME_KEY_{}".format(n))  # os.environ.get("ACME_KEY_%s" % n) in Python 2


def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "{filename}.{ext}".format(filename=uuid.uuid4(), ext=ext)
    return os.path.join('sticker_files', filename)


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
    upload = models.FileField("file", blank=True, upload_to=get_file_path)

    #class Meta:
        #ordering = ['-votes']

    def __unicode__(self):
        return self.title


class StickerVote(models.Model):
    sticker = models.ForeignKey(Sticker, related_name="votes")
    user = models.OneToOneField(User)

    def __unicode__(self):
        return '-'.join(['Vote', self.sticker.title])
