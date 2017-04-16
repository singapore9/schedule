from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Lesson, LessonName, LessonTime, Group, Teacher


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', )


class LessonNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonName
        fields = ('name', )


class LessonTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonTime
        fields = ('beginning_at', 'ended_at',)


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('name', )


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ('full_name', )


class LessonSerializer(serializers.ModelSerializer):
    group = GroupSerializer()
    name = LessonNameSerializer()
    period = LessonTimeSerializer()
    teacher = TeacherSerializer()

    class Meta:
        model = Lesson
        fields = ('group', 'name', 'type', 'note', 'date', 'period', 'teacher', )
