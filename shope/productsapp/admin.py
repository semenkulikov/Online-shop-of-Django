from django.contrib import admin

from productsapp.models.product import Product
from productsapp.models.comment import Comment
from productsapp.models.discount import Discount
from productsapp.models.category import Category
from productsapp.models.specific import Specific
from productsapp.models.type_spec import TypeSpecific


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


admin.site.register(Comment)
admin.site.register(Discount)
admin.site.register(Category)
admin.site.register(Specific)
admin.site.register(TypeSpecific)
