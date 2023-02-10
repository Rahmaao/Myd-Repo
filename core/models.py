from django.db import models
from django.core.validators import MinValueValidator
from django.db.models.deletion import CASCADE, PROTECT
from django.contrib.postgres.fields import ArrayField

# from django.contrib.auth.models import AbstractUser

# Create your models here.


class Person(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    marks = models.IntegerField()


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=PROTECT)
    name = models.CharField(max_length=255)
    description = models.TextField()
    sku = models.IntegerField()
    product_price = models.IntegerField()
    discount = models.IntegerField()
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    @property
    def discounted_price(self):
        return ((self.product_price) * (self.discount)) / 100

    @property
    def sale_price(self):
        return (self.product_price) - (self.discounted_price)

    @property
    def in_stock(self):
        return False if (self.is_available == 0) else (self.in_stock) == True

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=PROTECT)
    image = models.ImageField(upload_to="images/")

    def __str__(self):
        return self.image


class ProductSize(models.Model):
    product = models.ForeignKey(Product, on_delete=CASCADE)
    size = models.CharField(max_length=255)

    def __str__(self):
        return self.size


class ProductColor(models.Model):
    product = models.ForeignKey(Product, on_delete=CASCADE)
    color = models.CharField(max_length=255)

    def __str__(self):
        return self.color
