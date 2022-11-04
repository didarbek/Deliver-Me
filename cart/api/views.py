from django.shortcuts import get_object_or_404

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from cart.models import Cart, CartProduct
from cart.api.serializers import CartSerializer, CartProductSerializer
from users.models import Address


class CartRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        queryset = self.get_queryset()
        cart = get_object_or_404(queryset, user=self.request.user)
        return cart


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_cart(request):
    check = CartProduct.objects.filter(
        cart=request.user.cart,
        product_id=request.POST.get('product')
    ).exists()

    if check:
        cart_product = CartProduct.objects.get(
            cart=request.user.cart,
            product_id=request.POST.get('product')
        )
        cart_product.quantity += 1
        cart_product.save()
    else:
        cart_product = CartProduct.objects.create(
            cart=request.user.cart,
            product_id=request.POST.get('product')
        )
        cart_product.save()

    serializer = CartProductSerializer(cart_product)
    return Response({
        'message': 'Product has been successfully added to your cart.',
        'data': serializer.data
    }, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_from_cart(request):
    cart_product = get_object_or_404(CartProduct, product_id=request.POST.get('product'))
    serializer = CartProductSerializer(cart_product)

    if cart_product.cart.user == request.user:
        if cart_product.quantity > 1:
            cart_product.quantity -= 1
            cart_product.save()
            return Response({
                'message': 'Product quantity has been successfully updated.',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        else:
            cart_product.delete()
            return Response({
                'message': 'Product has been successfully deleted from the cart.',
                'data': serializer.data
            }, status=status.HTTP_200_OK)

    return Response('You are not allowed to make this action!', status=status.HTTP_403_FORBIDDEN)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_paid_orders(request):
    cart = get_object_or_404(Cart, user=request.user)
    paid_orders = cart.c_products.all().filter(is_paid=True)

    serializer = CartProductSerializer(data=paid_orders, many=True)
    serializer.is_valid()

    return Response({
        'message': 'Here is your paid orders.',
        'data': serializer.data
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    orders = cart.c_products.all()
    total = 0
    for order in orders:
        if not order.is_paid:
            order_total = order.get_total()
            total += order_total

    if request.user.addresses.exists():
        address = Address.objects.filter(user=request.user).first()
    else:
        address = Address.objects.create(
            user=request.user,
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            address1=request.POST.get('address1'),
            address2=request.POST.get('address2'),
            zip_code=request.POST.get('zip_code'),
            country=request.POST.get('country'),
            city=request.POST.get('city')
        )
        address.save()

    for order in orders:
        order.is_paid = True
        order.save()

    return Response('Success')