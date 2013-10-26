from django import forms
from django.contrib.admin.widgets import AdminFileWidget

from markitup.widgets import MarkItUpWidget

from .models import Sticker

class StickerForm(forms.ModelForm):
    class Meta:
        model = Sticker
        fields = [
            "title",
            "description",
            "upload"
        ]
        widgets = {
            "description": MarkItUpWidget(),
            "upload": AdminFileWidget(),
        }
