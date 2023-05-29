# Generated by Django 4.2.1 on 2023-05-29 10:48

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0004_userttype_remove_user_is_staff_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="is_admin",
        ),
        migrations.AddField(
            model_name="user",
            name="is_staff",
            field=models.BooleanField(default=False),
        ),
    ]
