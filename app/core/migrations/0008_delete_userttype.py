# Generated by Django 4.2.1 on 2023-05-29 17:55

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0007_brandname_category_product"),
    ]

    operations = [
        migrations.DeleteModel(
            name="UsertType",
        ),
    ]
