# Generated by Django 4.2.2 on 2023-08-12 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_remove_userprofile_managed_store'),
    ]

    operations = [
        migrations.AddField(
            model_name='appuser',
            name='is_super',
            field=models.BooleanField(default=False),
        ),
    ]
