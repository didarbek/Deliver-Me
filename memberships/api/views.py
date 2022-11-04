from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from memberships.models import Membership, UserMembership
from memberships.api.serializers import MembershipSerializer, UserMembershipSerializer


class MembershipsListAPIView(ListAPIView):
    queryset = Membership.objects.all()
    serializer_class = MembershipSerializer
    permission_classes = (AllowAny,)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_premium_membership(request):
    user_membership = get_object_or_404(UserMembership, user=request.user)

    if user_membership.membership.membership_type == 'Premium':
        return Response('You already have premium membership.', status=status.HTTP_200_OK)

    premium_membership = Membership.objects.get(membership_type='Premium')

    user_membership.membership = premium_membership
    user_membership.save()

    serializer = UserMembershipSerializer(user_membership)

    return Response({
        'message': 'You have successfully switched your plan to premium.',
        'data': serializer.data
    }, status=status.HTTP_200_OK)
