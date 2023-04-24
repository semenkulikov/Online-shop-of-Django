from django.contrib import admin
from productsapp.models.product import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Регистрация модели Product в админ-панели
    """
    list_display = ["pk",
                    "name",
                    "description",
                    "price",
                    "image",
                    "tags",
                    "archived",
                    "is_delivered",
                    ]

    ordering = "-price", "name", "archived", "is_delivered"
