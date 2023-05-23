# Generated by Django 4.2 on 2023-05-18 15:59
# flake8: noqa
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('productsapp', '0007_alter_review_product_alter_review_user'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('profileapp', '0006_alter_profile_avatar_image_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ViewedProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='viewed_by_users', to='productsapp.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='viewed_products', to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name': 'viewed product',
                'verbose_name_plural': 'viewed products',
            },
        ),
    ]