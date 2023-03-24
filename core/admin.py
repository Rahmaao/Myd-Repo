from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(
    [Student, Product, Category, ProductVariantMetadata, ProductVariantCombination, ColorVariant, SizeVariant,
     MaterialVariant])
