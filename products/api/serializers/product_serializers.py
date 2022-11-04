from rest_framework import serializers

from products.models import (
    Product,
    ProductCategory,
    DeliveryType,
    ProductImage,
    ProductVideo,
    BrowsingHistory
)
from products.api.serializers.product_question_serializers import ProductQuestionSerializer
from products.api.serializers.product_review_serializers import ProductReviewSerializer


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = '__all__'
        extra_kwargs = {
            'image': {'required': True},
            'product': {'required': True}
        }

    def validate(self, data):
        request = self.context['request']
        if data['product'].seller != request.user:
            raise serializers.ValidationError('You are not allowed to do this action')

        return data

    def create(self, validated_data):
        product_image = ProductImage.objects.create(
            image=validated_data['image'],
            product=validated_data['product']
        )
        product_image.save()

        return product_image


class ProductVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVideo
        fields = '__all__'
        extra_kwargs = {
            'video': {'required': True},
            'product': {'required': True}
        }

    def validate(self, data):
        request = self.context['request']
        if data['product'].seller != request.user:
            raise serializers.ValidationError('You are not allowed to do this action')

        return data

    def create(self, validated_data):
        product_video = ProductVideo.objects.create(
            video=validated_data['video'],
            product=validated_data['product']
        )
        product_video.save()

        return product_video


class DeliveryTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryType
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    total_price = serializers.SerializerMethodField('get_total_price')
    tags = serializers.SerializerMethodField('get_tags')
    seller = serializers.SerializerMethodField('get_seller')
    delivery_type = DeliveryTypeSerializer(read_only=True)
    questions = ProductQuestionSerializer(read_only=True, many=True)
    reviews = ProductReviewSerializer(read_only=True, many=True)
    rating = serializers.DecimalField(max_digits=10, decimal_places=2, source='get_rating')

    class Meta:
        model = Product
        fields = '__all__'

    def create(self, validated_data):
        return Product.objects.create(**validated_data)

    def get_total_price(self, obj):
        if obj.discount and obj.price:
            discount_amount = (obj.price * obj.discount) / 100
            total_price = round(obj.price - discount_amount, 2)
            return total_price
        return obj.price

    def get_tags(self, obj):
        if obj.tags:
            tags = []
            for tag in obj.tags.all():
                tags.append(tag.title)
            return tags
        return None

    def get_seller(self, obj):
        if obj.seller:
            return {
                'id': obj.seller.id,
                'email': obj.seller.email,
                'first_name': obj.seller.first_name,
                'last_name': obj.seller.last_name,
            }
        return None


class ProductCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductCategory
        fields = '__all__'


class ProductCategoryTreeSerializer(ProductCategorySerializer):
    parent = ProductCategorySerializer(read_only=True)
    children = serializers.SerializerMethodField('get_children')

    class Meta(ProductCategorySerializer.Meta):
        fields = '__all__'

    def get_children(self, obj):
        """
        Method to get category's children categories
        @param obj:
        @return:
        """
        child_category = ProductCategory.objects.filter(parent=obj)
        queue = list(child_category)
        children = []
        while len(queue):
            next_children = ProductCategory.objects.filter(parent=queue[0])
            child_category = child_category.union(next_children)
            queue.pop(0)
            queue = queue + list(next_children)
        for category in child_category:
            children.append(category.title)
        return children


class BrowsingHistorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(read_only=True, many=True)

    class Meta:
        model = BrowsingHistory
        fields = '__all__'
