# Generated by Django 3.2 on 2021-05-01 11:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_watchlist'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Watchlist',
        ),
    ]
