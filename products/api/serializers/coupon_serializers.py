from rest_framework import serializers

from products.models import Coupon


class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = '__all__'
        extra_kwargs = {
            'seller': {'required': False},
            'code': {'required': False}
        }
