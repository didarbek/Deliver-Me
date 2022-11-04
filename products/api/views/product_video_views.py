from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from products.models import ProductVideo
from products.api.serializers.product_serializers import ProductVideoSerializer


class ProductVideoCreateAPIView(generics.CreateAPIView):
    queryset = ProductVideo.objects.all()
    serializer_class = ProductVideoSerializer
    permission_classes = (IsAuthenticated,)


class ProductVideoDeleteAPIView(generics.DestroyAPIView):
    serializer_class = ProductVideoSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'id'

    def get_queryset(self):
        queryset = ProductVideo.objects.filter(id=self.kwargs['id'])
        return queryset

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.product.seller == request.user or request.user.is_superuser:
            self.perform_destroy(instance)
            return Response('Your video has been successfully removed from the product.', status=status.HTTP_200_OK)

        return Response('You are not allowed to do this action', status=status.HTTP_400_BAD_REQUEST)
