from rest_framework import serializers

from products.models import Wishlist
from products.api.serializers.product_serializers import ProductSerializer
from users.api.serializers import UserSerializer


class WishlistSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    wished_products = ProductSerializer(many=True)
    wishes_count = serializers.SerializerMethodField('get_wishes_count')

    class Meta:
        model = Wishlist
        fields = '__all__'

    def get_wishes_count(self, obj):
        return obj.wished_products.all().count()
