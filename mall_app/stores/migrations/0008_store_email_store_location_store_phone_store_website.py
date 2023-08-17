# Generated by Django 4.2.2 on 2023-08-12 21:03

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stores', '0007_storecategory_rename_category_itemcategory_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='store',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, validators=[django.core.validators.EmailValidator()]),
        ),
        migrations.AddField(
            model_name='store',
            name='location',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='store',
            name='phone',
            field=models.CharField(blank=True, max_length=20, null=True, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')]),
        ),
        migrations.AddField(
            model_name='store',
            name='website',
            field=models.URLField(blank=True, null=True, validators=[django.core.validators.URLValidator()]),
        ),
    ]