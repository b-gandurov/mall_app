# Generated by Django 4.2.2 on 2023-08-11 10:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stores', '0006_item_reservation_timer'),
    ]

    operations = [
        migrations.CreateModel(
            name='StoreCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RenameModel(
            old_name='Category',
            new_name='ItemCategory',
        ),
        migrations.AddField(
            model_name='store',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='stores', to='stores.storecategory'),
        ),
    ]
