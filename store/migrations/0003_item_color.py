# Generated by Django 3.1.3 on 2020-12-18 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_item_size'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='color',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
