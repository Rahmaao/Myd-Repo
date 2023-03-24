from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.db import models
# from django.core.validators import MinValueValidator
from django.db.models.deletion import CASCADE
from django.urls import reverse
# from django.contrib.postgres.fields import ArrayField
from django.utils import timezone
from slugify import slugify
from core.utils import get_variant_combination

# Create your models here.
from core.utils import generate_string_of_length


# from django.contrib.auth.models import AbstractUser


class Student(models.Model):
    name = models.CharField(max_length=155)
    age = models.IntegerField()


class Person(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    marks = models.IntegerField()
    created_by = models.ForeignKey(User, on_delete=CASCADE)


class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    date = models.DateTimeField(default=timezone.now)

    def get_absolute_url(self):
        return reverse('category-detail', kwargs={'pk': self.pk})

    @property
    def product_count(self):
        return self.product_set.all().count()

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    sku = models.CharField(max_length=15, null=True, blank=True, unique=True)
    product_price = models.IntegerField(default=0)
    color = models.CharField(max_length=255, null=True, blank=True)
    size = models.CharField(max_length=255, null=True, blank=True)
    manufacturer = models.CharField(max_length=255, null=True, blank=True)
    brand = models.CharField(max_length=255, null=True, blank=True)
    dimension = models.CharField(max_length=255, null=True, blank=True)
    weight = models.CharField(max_length=255, null=True, blank=True)
    discount = models.IntegerField(default=0, null=True, blank=True)
    tax = models.IntegerField(default=0, null=True, blank=True)
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('product_details', kwargs={'pk': self.pk})

    @property
    def variants(self):
        return ProductVariantCombination.objects.filter(product=self)

    def generate_variant_combinations(self):

        color_variant_metadata = ProductVariantMetadata.objects.filter(product=self, variant_name='color').first()
        size_variant_metadata = ProductVariantMetadata.objects.filter(product=self, variant_name='size').first()
        material_variant_metadata = ProductVariantMetadata.objects.filter(product=self,
                                                                          variant_name='material').first()

        color_variants = ColorVariant.objects.filter(product_variant_metadata=color_variant_metadata)
        size_variants = SizeVariant.objects.filter(product_variant_metadata=size_variant_metadata)
        material_variants = MaterialVariant.objects.filter(product_variant_metadata=material_variant_metadata)

        variant_combinations = get_variant_combination(color_variants, size_variants, material_variants)

        for variant_combination in variant_combinations:
            color = variant_combination[0]
            size = variant_combination[1]
            material = variant_combination[2]

            ProductVariantCombination.objects.create(color_variants=color, size_variants=size,
                                                     material_variants=material)

    def save(self, **kwargs):
        if not self.pk:
            slug = slugify(self.name)
            sku_first_half = slug[:5]
            sku_second_half = generate_string_of_length(5)

            candidate_sku = f"{sku_first_half}{sku_second_half}"

            product = Product.objects.filter(sku=candidate_sku).first()

            while product is not None:
                sku_second_half = generate_string_of_length(5)
                candidate_sku = f"{sku_first_half}{sku_second_half}"
                product = Product.objects.filter(sku=candidate_sku).first()

            self.sku = candidate_sku

        super(Product, self).save(**kwargs)

    @property
    def discounted_price(self):
        return (self.product_price * self.discount) / 100

    @property
    def tax_price(self):
        return self.product_price * self.tax / 100

    @property
    def sale_price(self):
        return self.product_price - self.discounted_price + self.tax_price

    @property
    def in_stock(self):
        return self.stock > 0

    @property
    def is_listed(self):
        return self.in_stock and self.is_available

    def __str__(self):
        return self.name



class ColorVariant(models.Model):
    product_variant_metadata = models.ForeignKey('ProductVariantMetadata', on_delete=CASCADE)
    color_name = models.CharField(max_length=155)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['product_variant_metadata', 'color_name'],
                                    name='unique_together__color_variant__variant_metadata_color_name')
        ]


class SizeVariant(models.Model):
    product_variant_metadata = models.ForeignKey('ProductVariantMetadata', on_delete=CASCADE)
    size_name = models.CharField(max_length=255)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['product_variant_metadata', 'size_name'],
                                    name='unique_together__color_variant__variant_metadata_size_name')
        ]


class MaterialVariant(models.Model):
    product_variant_metadata = models.ForeignKey('ProductVariantMetadata', on_delete=CASCADE)
    material_name = models.CharField(max_length=255)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['product_variant_metadata', 'material_name'],
                                    name='unique_together__color_variant__variant_metadata_material_name')
        ]


class ProductVariantMetadata(models.Model):
    VARIANT_CHOICES = [
        ("COLOR", "COLOR"),
        ("SIZE", "SIZE"),
        ("MTRL", "MATERIAL"),
    ]

    product = models.ForeignKey(Product, on_delete=CASCADE)
    variant_name = models.CharField(
        max_length=10, choices=VARIANT_CHOICES, default="COLOR"
    )
    options = ArrayField(models.CharField(max_length=200), blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['variant_name', 'product'],
                                    name='unique_together__color_variant__variant_metadata_product')
        ]

    def __str__(self):
        return self.product.name

    def save(self, **kwargs):
        self.variant_name = self.variant_name.lower()
        super(ProductVariantMetadata, self).save(**kwargs)

    def create_variants(self):

        if self.variant_name == 'color':
            for option in self.options:
                ColorVariant.objects.create(color_name=option, product_variant_metadata=self)

        if self.variant_name == 'size':
            for option in self.options:
                SizeVariant.objects.create(size_name=option, product_variant_metadata=self)

        if self.variant_name == 'material':
            for option in self.options:
                MaterialVariant.objects.create(material_name=option, product_variant_metadata=self)


class ProductVariantCombination(models.Model):
    product = models.ForeignKey(Product, on_delete=CASCADE)
    color_variant = models.ForeignKey(ColorVariant, on_delete=CASCADE, blank=True, null=True)
    size_variant = models.ForeignKey(SizeVariant, on_delete=CASCADE, blank=True, null=True)
    material_variant = models.ForeignKey(MaterialVariant, on_delete=CASCADE, blank=True, null=True)
    price = models.FloatField(default=0)
    sku = models.CharField(blank=True, null=True, max_length=10)


    def get_absolute_url(self):
        return reverse('product-details', kwargs={'pk': self.pk})
