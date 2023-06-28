from django.core.cache import cache
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse


def clear_cache(request: HttpRequest, cache_name: str) -> HttpResponse:
    """ Представление для очистки кеша """
    if cache.get(cache_name, None):
        cache.delete(cache_name)
    elif cache_name == "total":
        cache.clear()
    return redirect(reverse("coreapp:index"))
