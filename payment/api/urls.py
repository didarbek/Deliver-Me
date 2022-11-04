from django.urls import path

from payment.api.views import test_payment

app_name = 'payment'

urlpatterns = [
    path('test-payment/', test_payment, name='test_payment'),
]
