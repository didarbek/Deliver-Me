from rest_framework import serializers

from memberships.models import Membership, UserMembership, Subscription


class MembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membership
        fields = '__all__'


class UserMembershipSerializer(serializers.ModelSerializer):
    membership = MembershipSerializer(read_only=True)

    class Meta:
        model = UserMembership
        fields = '__all__'
