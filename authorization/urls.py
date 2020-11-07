from django.urls import path

from rest_framework.authtoken.views import obtain_auth_token
from .views import get_me

urlpatterns = [
    path('token', obtain_auth_token, name='token'),
    path('me', get_me, name='me')
]
