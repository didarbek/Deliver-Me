from django.urls import path

from memberships.api.views import (
    MembershipsListAPIView,
    get_premium_membership
)

app_name = 'memberships'

urlpatterns = [
    path('memberships/', MembershipsListAPIView.as_view(), name='memberships'),
    path('go_premium/', get_premium_membership, name='go_premium'),
]
