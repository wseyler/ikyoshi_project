# Generated by Django 3.1.3 on 2020-12-04 18:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0001_initial'),
        ('ranks', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rank',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('test_date', models.DateField()),
                ('award_date', models.DateField()),
                ('tested', models.BooleanField(default=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('martial_artist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='people.martialartist')),
                ('rank_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ranks.ranktype')),
            ],
        ),
    ]
