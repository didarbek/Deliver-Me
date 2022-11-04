from django.shortcuts import get_object_or_404

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

from products.models import ProductReview
from products.api.serializers.product_review_serializers import ProductReviewSerializer
from products.api.permissions import IsReviewAuthorOrReadOnly


class ProductReviewCreateAPIView(generics.CreateAPIView):
    queryset = ProductReview.objects.all()
    serializer_class = ProductReviewSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ProductReviewUpdateAPIView(generics.UpdateAPIView):
    queryset = ProductReview.objects.all()
    serializer_class = ProductReviewSerializer
    permission_classes = (IsReviewAuthorOrReadOnly,)
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductReviewDeleteAPIView(generics.DestroyAPIView):
    serializer_class = ProductReviewSerializer
    permission_classes = (IsReviewAuthorOrReadOnly,)
    lookup_field = 'id'

    def get_queryset(self):
        queryset = ProductReview.objects.filter(id=self.kwargs['id'])
        return queryset

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response('Your review has been successfully deleted.', status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def review_is_helpful(request):
    review = get_object_or_404(ProductReview, id=request.POST.get('review'))
    is_helpful = False
    if review.found_helpful.filter(id=request.user.id).exists():
        review.found_helpful.remove(request.user)
        is_helpful = False
    else:
        review.found_helpful.add(request.user)
        is_helpful = True

    serializer = ProductReviewSerializer(review)

    return Response(serializer.data, status=status.HTTP_200_OK)
