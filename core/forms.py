
from django import forms
from .models import *

from django.utils.translation import gettext_lazy as _


import re


class PersonForm(forms.Form):
    class meta:
        model = Person
        fields = '__all__'



class CategoryForm(forms.Form):
    name = forms.CharField


class ProductForm(forms.Form):
    name = forms.CharField
    category = models.ForeignKey
    name = models.CharField
    description = models.TextField
    sku = models.IntegerField
    product_price = models.IntegerField
    color = models.CharField
    size = models.CharField
    manufacturer = models.CharField
    brand = models.CharField
    dimension = models.CharField
    weight = models.CharField
    discount = models.IntegerField
    stock = models.IntegerField
    # tax = models.IntegerField
    is_available = models.BooleanField
    created_date = models.DateTimeField
    modified_date = models.DateTimeField