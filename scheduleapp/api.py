import datetime
from django.contrib.auth.models import User
from rest_framework import mixins
from rest_framework import viewsets

from .models import Lesson, LessonDate
from .serializers import UserSerializer, LessonSerializer, DaySerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ScheduleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = LessonDate.objects.all()
    serializer_class = DaySerializer

    def get_queryset(self):
        date_from = self.request.query_params.get('date_from')
        date_from = datetime.datetime.strptime(date_from, '%Y-%m-%d').date()
        date_to = self.request.query_params.get('date_to')
        date_to = datetime.datetime.strptime(date_to, '%Y-%m-%d').date()
        group_id = int(self.request.query_params.get('group_id'))
        items = LessonDate.objects.filter(date__gte=date_from, date__lt=date_to, group_id=group_id).order_by('date')
        return items