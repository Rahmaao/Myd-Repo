# Generated by Django 4.1.7 on 2023-03-10 10:19

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="productvariantmetadata",
            unique_together={("variant_name", "product")},
        ),
    ]
