from django.shortcuts import get_object_or_404

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from products.models import Coupon
from products.api.serializers.coupon_serializers import CouponSerializer


class CurrentUserCouponsListAPIView(generics.ListAPIView):
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        coupons = Coupon.objects.filter(seller=self.request.user)
        return coupons


class CouponCreateAPIView(generics.CreateAPIView):
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(
            seller=self.request.user,
            code=Coupon.generate_code()
        )


class CouponUpdateAPIView(generics.UpdateAPIView):
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        if instance.seller == request.user or request.user.is_superuser:
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)

        return Response('You are not allowed to to this action', status=status.HTTP_403_FORBIDDEN)


class CouponDeleteAPIView(generics.DestroyAPIView):
    serializer_class = CouponSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'id'

    def get_queryset(self):
        queryset = Coupon.objects.filter(id=self.kwargs['id'])
        return queryset

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.seller == request.user or request.user.is_superuser:
            self.perform_destroy(instance)
            return Response('Your coupon has been successfully deleted', status=status.HTTP_200_OK)

        return Response('You are not allowed to do this action', status=status.HTTP_403_FORBIDDEN)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def redeem_coupon(request):
    coupon = get_object_or_404(Coupon, id=request.POST.get('coupon'))
    serializer = CouponSerializer(coupon)
    is_redeemed = False
    if coupon.users.filter(id=request.user.id).exists():
        is_redeemed = True
        return Response({
            'message': 'You already redeemed this coupon',
            'is_redeemed': is_redeemed,
            'coupon': serializer.data
        }, status=status.HTTP_400_BAD_REQUEST)
    else:
        coupon.users.add(request.user)
        is_redeemed = True

    return Response(serializer.data, status=status.HTTP_200_OK)
