from django.shortcuts import get_object_or_404

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated


from products.models import Wishlist
from products.api.serializers.wishlist_serializers import WishlistSerializer


class WishlistRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        queryset = self.get_queryset()
        wishlist = get_object_or_404(queryset, user=self.request.user)
        return wishlist


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_remove_wishlist(request):
    wishlist = get_object_or_404(Wishlist, user=request.user)
    product = request.POST.get('product')
    is_in_wishlist = False

    if wishlist.wished_products.filter(id=product).exists():
        wishlist.wished_products.remove(product)
        is_in_wishlist = False
    else:
        wishlist.wished_products.add(product)
        is_in_wishlist = True

    serializer = WishlistSerializer(wishlist)

    return Response({
        'wishlist': serializer.data,
        'is_in_wishlist': is_in_wishlist
    }, status=status.HTTP_200_OK)
