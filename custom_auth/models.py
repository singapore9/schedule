from django.db import models

from scheduleapp.models import Lesson


class ApplicationUser(models.Model):
    email = models.EmailField(unique=True, blank=False, null=False)
    first_name = models.CharField(null=True, max_length=256)
    last_name = models.CharField(null=True, max_length=256)
    visited_lessons = models.ManyToManyField(Lesson, related_name='visitors')
    unvisited_lessons = models.ManyToManyField(Lesson, related_name='slackers')

    def __str__(self):
        return '[%s] %s %s' % (self.email, self.last_name, self.first_name)
