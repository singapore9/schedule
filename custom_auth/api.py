from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny

from custom_auth.utils import get_user_info
from .models import Token, ApplicationUser
from .serializers import VkTokenSerializer


class VkTokenViewSet(mixins.RetrieveModelMixin,
                     mixins.CreateModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.ListModelMixin,
                     viewsets.GenericViewSet):
    permission_classes = [AllowAny, ]
    serializer_class = VkTokenSerializer
    queryset = Token.objects
    http_method_names = ['get', ]

    def get_queryset(self):
        code = self.request.GET['code']
        user_info = get_user_info(code)

        if not user_info.get('error', None):
            token = Token.objects.create(token=user_info['access_token'],
                                         auth_type=Token.AUTH_WITH_VK,
                                         expires_in=user_info['expires_in'])

            user, _ = ApplicationUser.objects.get_or_create(email=user_info['email'])
            # user.tokens.all().delete()
            user.tokens.add(token)
            user.save()

        return Token.objects.all()
