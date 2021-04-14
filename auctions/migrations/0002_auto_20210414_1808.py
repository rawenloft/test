# Generated by Django 3.2 on 2021-04-14 18:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bids',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='bid id')),
                ('start_bid', models.IntegerField(default='1')),
                ('highest_bid', models.IntegerField(default='1')),
                ('started_at', models.DateTimeField(auto_now_add=True, verbose_name=['%d-%m-%Y %H:%M:%S'])),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bidder', to=settings.AUTH_USER_MODEL)),
                ('highest_bidder', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='winner', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='listing',
            name='start_bid',
            field=models.ForeignKey(default=True, on_delete=django.db.models.deletion.CASCADE, related_name='starting_bid', to='auctions.bids'),
        ),
    ]
