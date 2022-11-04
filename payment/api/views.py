import os
import stripe
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response


stripe.api_key = os.getenv("STRIPE_SECRET_KEY")


@api_view(['POST'])
def test_payment(request):
    test_payment_intent = stripe.PaymentIntent.create(
        amount=1000, currency='pln',
        payment_method_types=['card'],
        receipt_email='test@example.com'
    )

    return Response(data=test_payment_intent, status=status.HTTP_200_OK)


@api_view(['POST'])
def save_stripe_info(request):
    data = request.data
    email = data['email']
    payment_method_id = data['payment_method_id']
    extra_msg = ''

    customer_data = stripe.Customer.list(email=email).data

    if len(customer_data) == 0:
        customer = stripe.Customer.create(
            email=email,
            payment_method=payment_method_id
        )
    else:
        customer = customer_data[0]
        extra_msg = 'Customer already existed.'

    return Response(data={
        'message': 'Success',
        'data': {
            'customer_id': customer.id,
            'extra_msg': extra_msg
        }
    }, status=status.HTTP_200_OK)
