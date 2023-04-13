from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

app_name = 'paymentapp'

urlpatterns = [
    path('payment/', TemplateView.as_view(template_name=
                                          "paymentapp/payment.html")),
    path('paymentsomeone/', TemplateView.as_view(template_name=
                                                 "paymentapp/paymentsomeone.html")),
    path('progressPayment/', TemplateView.as_view(template_name=
                                                  "paymentapp/progressPayment.html")),

]
