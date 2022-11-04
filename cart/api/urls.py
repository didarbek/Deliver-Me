from django.urls import path

from cart.api.views import (
    CartRetrieveAPIView,
    add_to_cart,
    remove_from_cart,
    get_paid_orders,
    checkout
)


app_name = 'cart'

urlpatterns = [
    path('cart/', CartRetrieveAPIView.as_view(), name='cart'),
    path('cart/add/', add_to_cart, name='cart_add'),
    path('cart/remove/', remove_from_cart, name='cart_remove'),
    path('orders/', get_paid_orders, name='orders'),
    path('checkout/', checkout, name='checkout'),
]
