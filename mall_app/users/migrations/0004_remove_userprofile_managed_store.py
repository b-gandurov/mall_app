# Generated by Django 4.2.2 on 2023-08-11 09:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_userprofile_managed_store'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='managed_store',
        ),
    ]