from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models

from scheduleapp.models import Lesson


class ApplicationUser(AbstractBaseUser):
    username = models.CharField(null=False, max_length=256)
    email = models.EmailField(unique=True, blank=False, null=False)
    first_name = models.CharField(null=True, max_length=256)
    last_name = models.CharField(null=True, max_length=256)
    visited_lessons = models.ManyToManyField(Lesson, related_name='visitors')
    unvisited_lessons = models.ManyToManyField(Lesson, related_name='slackers')

    USERNAME_FIELD = 'email'

    def __str__(self):
        return '[%s] %s %s' % (self.email, self.last_name, self.first_name)


class Token(models.Model):
    AUTH_WITH_VK = 0
    AUTH_WITH_GOOGLE = 1
    auth_choices = (
        (AUTH_WITH_VK, 'vk'),
        (AUTH_WITH_GOOGLE, 'google')
    )

    auth_type = models.PositiveSmallIntegerField(choices=auth_choices)
    token = models.CharField(null=False, max_length=200)
    user = models.ForeignKey(ApplicationUser, related_name='tokens', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_in = models.PositiveIntegerField(default=86402)
