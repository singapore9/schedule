import datetime
from rest_framework import mixins
from rest_framework import viewsets

from .models import LessonDate, Group, University
from .serializers import DaySerializer, UniversitySerializer
from .bsuir_lessons import get_schedule_for


class ScheduleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = LessonDate.objects.all()
    serializer_class = DaySerializer

    def get_queryset(self):
        date_from = self.request.query_params.get('date_from')
        date_from = datetime.datetime.strptime(date_from, '%Y-%m-%d').date()
        date_to = self.request.query_params.get('date_to')
        date_to = datetime.datetime.strptime(date_to, '%Y-%m-%d').date()
        group_id = int(self.request.query_params.get('group_id'))
        if LessonDate.objects.filter(group_id=group_id).count() == 0:
            try:
                get_schedule_for(Group.objects.get(id=group_id).local_id)
            except Exception as e:
                pass
        items = LessonDate.objects.filter(date__gte=date_from, date__lt=date_to, group_id=group_id).order_by('date')
        return items


class UniversityViewSet(mixins.ListModelMixin,
                        viewsets.GenericViewSet):
    http_method_names = ['get', ]
    queryset = University.objects.all()
    serializer_class = UniversitySerializer