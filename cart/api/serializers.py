from rest_framework import serializers

from cart.models import Cart, CartProduct
from users.models import Address
from products.models import Coupon
from users.api.serializers import UserSerializer


class CartProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = CartProduct
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    products = serializers.SerializerMethodField('get_cart_products')
    total = serializers.SerializerMethodField('get_total')

    class Meta:
        model = Cart
        fields = '__all__'

    def get_cart_products(self, obj):
        serializer = CartProductSerializer(obj.c_products, many=True)
        return serializer.data

    def get_total(self, obj):
        total = 0

        if obj.c_products:
            for t in obj.c_products.all():
                if not t.is_paid:
                    for i in range(t.quantity):
                        total += t.product.price
            return total

        return 0


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'address1': {'required': True},
            'address2': {'required': False},
            'zip_code': {'required': True},
            'country': {'required': True},
            'city': {'required': True}
        }
