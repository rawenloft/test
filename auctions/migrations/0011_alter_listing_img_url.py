# Generated by Django 3.2 on 2021-05-03 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0010_alter_listing_img_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='img_url',
            field=models.URLField(default='https://thumbs.dreamstime.com/b/new-product-grunge-vintage-stamp-isolated-white-background-new-product-sign-new-product-stamp-153380133.jpg'),
        ),
    ]
