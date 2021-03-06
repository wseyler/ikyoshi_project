# Generated by Django 3.1.3 on 2020-12-18 19:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('make', models.CharField(blank=True, max_length=50, null=True)),
                ('sku', models.CharField(blank=True, max_length=30, null=True)),
                ('wholesale_price', models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True)),
                ('retail_price', models.DecimalField(decimal_places=2, max_digits=7)),
                ('quantity_on_hand', models.PositiveSmallIntegerField(default=0)),
                ('notes', models.TextField(blank=True, null=True)),
            ],
        ),
    ]
