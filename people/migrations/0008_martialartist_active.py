# Generated by Django 3.1.3 on 2020-12-06 23:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0007_auto_20201205_1206'),
    ]

    operations = [
        migrations.AddField(
            model_name='martialartist',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
