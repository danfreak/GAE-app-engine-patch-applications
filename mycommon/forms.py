# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from django.core.files.uploadedfile import UploadedFile
from django.utils.translation import ugettext_lazy as _, ugettext as __
from ragendja.auth.models import UserTraits
from ragendja.forms import FormWithSets, FormSetField


class FileForm(forms.ModelForm):
    name = forms.CharField(required=False, label='Name (set automatically)')

    def clean(self):
        file = self.cleaned_data.get('file')
        
        if not self.cleaned_data.get('name'):
            if isinstance(file, UploadedFile):
                self.cleaned_data['name'] = file.name
            else:
                del self.cleaned_data['name']
        return self.cleaned_data