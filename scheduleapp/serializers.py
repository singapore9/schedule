from rest_framework import serializers

from custom_auth.serializers import BaseApplicationUserSerializer
from .models import Lesson, LessonTime, LessonDate, University, Faculty, Group


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('name', 'id')


class FacultySerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=True)

    class Meta:
        model = Faculty
        fields = ('groups', 'name', 'id')


class UniversitySerializer(serializers.ModelSerializer):
    faculties = FacultySerializer(many=True)

    class Meta:
        model = University
        fields = ('faculties', 'name', 'id')


class LessonTimeSerializer(serializers.ModelSerializer):
    beginning_at = serializers.DateTimeField(format="%H:%M")
    ended_at = serializers.DateTimeField(format="%H:%M")

    class Meta:
        model = LessonTime
        fields = ('beginning_at', 'ended_at',)


class LessonSerializer(serializers.ModelSerializer):
    group = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    time = LessonTimeSerializer()
    teacher = serializers.SerializerMethodField()
    slackers = BaseApplicationUserSerializer(many=True)
    visitors = BaseApplicationUserSerializer(many=True)

    class Meta:
        model = Lesson
        fields = ('group', 'name', 'type', 'note', 'time', 'teacher', 'id', 'location', 'slackers', 'visitors')
        read_only_fields = ('id', )

    def get_group(self, instance):
        return instance.group.name

    def get_name(self, instance):
        return instance.name.name

    def get_teacher(self, instance):
        return instance.teacher.full_name if instance.teacher else None

    def get_date(self, instance):
        return instance.date.date


class DaySerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True)

    class Meta:
        model = LessonDate
        fields = ('date', 'lessons')
