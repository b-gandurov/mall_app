# Generated by Django 4.2.2 on 2023-07-12 14:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
        ('parking', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customercar',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.userprofile'),
        ),
    ]
