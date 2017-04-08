from rest_framework import serializers

from custom_auth.models import Token


class VkTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ('auth_type', 'token', 'expires_in', )
