from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from products.models import BrowsingHistory
from products.api.serializers.product_serializers import BrowsingHistorySerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_history(request):
    history = get_object_or_404(BrowsingHistory, user=request.user)
    serializer = BrowsingHistorySerializer(history)

    return Response({
        'message': 'History has been successfully received',
        'data': serializer.data
    })


def add_history_element(user_id: int, product_id: int):
    history = get_object_or_404(BrowsingHistory, user_id=user_id)
    serializer = BrowsingHistorySerializer(history)

    history.products.add(product_id)

    return Response({
        'message': 'Product has been successfully added to your history',
        'data': serializer.data
    }, status=status.HTTP_200_OK)
