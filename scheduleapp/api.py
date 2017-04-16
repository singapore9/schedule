from django.contrib.auth.models import User
from rest_framework import mixins
from rest_framework import viewsets

from .models import Lesson
from .serializers import UserSerializer
from .serializers import LessonSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class LessonsViewSet(mixins.ListModelMixin,
                     viewsets.GenericViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
