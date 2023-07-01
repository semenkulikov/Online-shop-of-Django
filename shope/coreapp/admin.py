from django.contrib import admin
from django.urls import path

from .models import ConfigModel
from django.core.cache import cache
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse


@admin.register(ConfigModel)
class ConfigModelAdmin(admin.ModelAdmin):
    """
    Регистрация модели ConfigModel в админ-панели
    """
    list_display = "pk", "name", "value"

    change_list_template = "coreapp/button_to_clear_cache.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "clear_cache/<str:cache_name>/",
                self.admin_site.admin_view(
                    self.clear_cache,
                ),
                name="clear_cache"
            ),
        ]
        return custom_urls + urls

    def clear_cache(self, request: HttpRequest, cache_name: str):
        """ Представление для очистки кеша """
        if cache.get(cache_name, None):
            cache.delete(cache_name)
        elif cache_name == "total":
            cache.clear()
        return HttpResponseRedirect("../../")
