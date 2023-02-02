from django.db import models
# from ckeditor_uploader.fields import R
from datetime import datetime
from django.contrib.auth.models import AbstractUser

# Create your models here.


class Person(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    marks = models.IntegerField()
                            