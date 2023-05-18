from django.shortcuts import render
from .models import Order


def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-order_date')
    return render(request, 'historyorder.html', {'orders': orders})

