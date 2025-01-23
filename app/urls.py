from django.urls import path
from . import views


urlpatterns = [
    path('', views.initiate_payment, name='initiate_payment'),
    path('check_payment_status', views.check_payment_status, name='check_payment_status')
]