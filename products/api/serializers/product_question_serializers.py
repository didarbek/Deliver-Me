from rest_framework import serializers

from products.models import ProductQuestion


class ProductQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductQuestion
        fields = '__all__'
        extra_kwargs = {
            'text': {'required': True},
            'user': {'required': False},
            'product': {'required': True},
            'answer': {'required': False}
        }

    def create(self, validated_data):
        product_question = ProductQuestion.objects.create(
            text=validated_data['text'],
            user=validated_data['user'],
            product=validated_data['product']
        )
        product_question.save()

        return product_question

    def update(self, instance, validated_data):
        instance.text = validated_data.get('text', instance.text)
        instance.save()

        return instance
