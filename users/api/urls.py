from django.urls import path
from rest_framework.authtoken import views

from users.api.views import (
    profile_details,
    register
)

app_name = 'users'

urlpatterns = [
    path('profile/', profile_details, name='profile'),
    path('login/', views.obtain_auth_token, name='api-token-auth'),
    path('register/', register, name='register'),
]