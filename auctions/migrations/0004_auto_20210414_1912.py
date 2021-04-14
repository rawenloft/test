# Generated by Django 3.2 on 2021-04-14 19:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_rename_bids_bid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bid',
            name='started_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True, verbose_name='comment id')),
                ('content', models.TextField(max_length=512)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='commenter', to=settings.AUTH_USER_MODEL)),
                ('rel_listing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_aim', to='auctions.listing')),
            ],
        ),
    ]
