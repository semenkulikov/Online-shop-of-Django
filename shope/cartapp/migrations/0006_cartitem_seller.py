# Generated by Django 4.2 on 2023-05-22 11:56
# flake8: noqa

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('productsapp', '0007_alter_review_product_alter_review_user'),
        ('cartapp', '0005_alter_cart_options_alter_cartitem_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='seller',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='items', to='productsapp.seller', verbose_name='seller'),
            preserve_default=False,
        ),
    ]
