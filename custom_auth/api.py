from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from custom_auth.models import ApplicationUser
from custom_auth.serializers import ApplicationUserSerializer
from scheduleapp.models import Lesson


class ApplicationUserViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny, ]

    queryset = ApplicationUser.objects.all()
    serializer_class = ApplicationUserSerializer

    @detail_route(methods=['POST', ])
    def visit(self, request, **kwargs):
        data = request.data
        lesson_id = data.get('lesson_id', None)
        if lesson_id:
            user = self.get_object()
            lesson = Lesson.objects.get(id=lesson_id)
            user.visited_lessons.add(lesson)
            user.unvisited_lessons.remove(lesson)
            user.save()
            return Response(status=201)
        return Response(status=400)


    @detail_route(methods=['POST', ])
    def slack(self, request, **kwargs):
        data = request.data
        lesson_id = data.get('lesson_id', None)
        if lesson_id:
            user = self.get_object()
            lesson = Lesson.objects.get(id=lesson_id)
            user.visited_lessons.remove(lesson)
            user.unvisited_lessons.add(lesson)
            user.save()
            return Response(status=201)
        return Response(status=400)
