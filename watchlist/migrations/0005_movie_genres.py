# Generated by Django 3.0.6 on 2020-06-01 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('watchlist', '0004_auto_20200601_2037'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='genres',
            field=models.ManyToManyField(to='watchlist.Genre'),
        ),
    ]