from django.conf.urls import url, include
from rest_framework import routers

from .api import ScheduleViewSet, UniversityViewSet
from custom_auth.api import ApplicationUserViewSet


router = routers.DefaultRouter()
router.register(r'schedule', ScheduleViewSet)
router.register(r'university', UniversityViewSet)
router.register(r'users', ApplicationUserViewSet)


test_api_patterns = [
    url(r'', include(router.urls))
]
