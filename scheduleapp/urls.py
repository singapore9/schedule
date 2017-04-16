from django.conf.urls import url, include
from rest_framework import routers

from .api import UserViewSet
from .api import LessonsViewSet


router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'lessons', LessonsViewSet)

test_api_patterns = [
    url(r'', include(router.urls))
]
