# Generated by Django 4.2 on 2023-05-08 13:33
# flake8: noqa

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('productsapp', '0006_alter_review_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Seller',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('name', models.CharField(max_length=100, verbose_name='name')),
            ],
            options={
                'verbose_name': 'seller',
                'verbose_name_plural': 'sellers',
            },
        ),
        migrations.RemoveField(
            model_name='product',
            name='is_delivered',
        ),
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.ForeignKey(default=0.08333333333333333, on_delete=django.db.models.deletion.DO_NOTHING, related_name='category_products', to='productsapp.category', verbose_name='category'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='free_delivery',
            field=models.BooleanField(default=False, verbose_name='free_delivery'),
        ),
        migrations.CreateModel(
            name='Slider',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('description', models.CharField(max_length=300, verbose_name='description')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_on_slider', to='productsapp.product', verbose_name='product')),
            ],
            options={
                'verbose_name': 'slider',
                'verbose_name_plural': 'sliders',
            },
        ),
        migrations.CreateModel(
            name='SlicePrice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('value', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='value')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_price', to='productsapp.product', verbose_name='product')),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='slice_price', to='productsapp.seller', verbose_name='seller')),
            ],
            options={
                'verbose_name': 'price slice',
                'verbose_name_plural': 'price slices',
            },
        ),
        migrations.CreateModel(
            name='SellerItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='seller_items', to='productsapp.product', verbose_name='product')),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='seller_items', to='productsapp.seller', verbose_name='seller')),
            ],
            options={
                'verbose_name': "seller's item",
                'verbose_name_plural': "seller's items",
            },
        ),
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('image', models.ImageField(upload_to='banners_images/', verbose_name='image')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='category_on_banner', to='productsapp.category', verbose_name='category')),
            ],
            options={
                'verbose_name': 'banner',
                'verbose_name_plural': 'banners',
            },
        ),
    ]
