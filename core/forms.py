from attr import fields
from django import forms
from .models import Member, Document, Ajax, CsvUpload, Person

from django.utils.translation import gettext_lazy as _
from ckeditor.widgets import CKEditorWidget


import re


class PersonForm(forms.Form):
    class meta:
        model = Person
        fields = '__all__'