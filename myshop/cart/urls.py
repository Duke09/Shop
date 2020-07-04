from django.urls import path

from .views import *

app_name = 'cart'

urlpatterns = [
    path('', cart_detail, name='cart_detail'),
    path('add/<int:product_id>/', cart_add, name='cart_add'),
    path('dec/<int:product_id>/', cart_dec, name='cart_dec'),
    path('remove/<int:product_id>/', cart_remove, name='cart_remove'),
]