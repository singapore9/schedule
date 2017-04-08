from django.conf.urls import url, include
from rest_framework import routers

from .api import VkTokenViewSet
from .views import vk_view

router = routers.DefaultRouter()
router.register(r'auth_vk', VkTokenViewSet)

urls = [
    url(r'vk/', view=vk_view)
]

auth_api_patterns = [
    url(r'', include(router.urls)),
]
