from django.conf.urls import url, include
from rest_framework import routers

from .api import UserViewSet
from .api import ScheduleViewSet


router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'schedule', ScheduleViewSet)

test_api_patterns = [
    url(r'', include(router.urls))
]
