# Generated by Django 3.1.3 on 2020-12-05 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0006_auto_20201205_1147'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sponsor',
            name='telephone',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]