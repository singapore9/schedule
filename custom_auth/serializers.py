from rest_framework import serializers

from custom_auth.models import ApplicationUser


class BaseApplicationUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationUser
        fields = ('email', 'first_name', 'last_name', 'id')
        read_only_fields = ('id', )


class ApplicationUserSerializer(BaseApplicationUserSerializer):
    class Meta(BaseApplicationUserSerializer.Meta):
        fields = BaseApplicationUserSerializer.Meta.fields + ('visited_lessons', 'unvisited_lessons')
        read_only_fields = BaseApplicationUserSerializer.Meta.read_only_fields + ('visited_lessons', 'unvisited_lessons')

