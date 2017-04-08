from django.conf.urls import url, include
from rest_framework import routers

from .views import UserViewSet


router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

test_api_patterns = [
    url(r'', include(router.urls))
]
