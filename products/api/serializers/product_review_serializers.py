from rest_framework import serializers

from products.models import ProductReview


class ProductReviewSerializer(serializers.ModelSerializer):
    found_helpful_count = serializers.SerializerMethodField('get_found_helpful_count')

    class Meta:
        model = ProductReview
        fields = '__all__'
        extra_kwargs = {
            'title': {'required': True},
            'description': {'required': True},
            'rating': {'required': True},
            'product': {'required': False},
            'author': {'required': False}
        }

    def create(self, validated_data):
        review = ProductReview.objects.create(
            title=validated_data['title'],
            description=validated_data['description'],
            rating=validated_data['rating'],
            product=validated_data['product'],
            author=validated_data['author']
        )
        review.save()

        return review

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.rating = validated_data.get('rating', instance.rating)
        instance.save()

        return instance

    def get_found_helpful_count(self, obj):
        return obj.found_helpful.count()
