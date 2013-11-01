from django import forms
from django.contrib.admin.widgets import AdminFileWidget
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as _

from markitup.widgets import MarkItUpWidget

from .models import Sticker

# 2.5MB - 2621440
# # 5MB - 5242880
# # 10MB - 10485760
# # 20MB - 20971520
# # 50MB - 5242880
# # 100MB - 104857600
# # 250MB - 214958080
# # 500MB - 429916160
MAX_UPLOAD_SIZE = 2621440


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

    def clean_upload(self):
        content = self.cleaned_data['upload']
        if content:
            if content._size > int(MAX_UPLOAD_SIZE):
                raise forms.ValidationError(_(u'Please keep filesize under %s. Current filesize %s') % (filesizeformat(MAX_UPLOAD_SIZE), filesizeformat(content._size)))
            return content
