from django.conf.urls import url, include
from rest_framework import routers

from .api import UserViewSet
from .api import ScheduleViewSet
from .api import UniversityViewSet


router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'schedule', ScheduleViewSet)
router.register(r'university', UniversityViewSet)

test_api_patterns = [
    url(r'', include(router.urls))
]
