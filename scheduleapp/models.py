import random

from django.db import models


class LocalIDMixin(models.Model):
    local_id = models.CharField(max_length=32, null=True, blank=True)

    class Meta:
        abstract = True


class NameMixin(models.Model):
    name = models.CharField(max_length=100, null=False)

    class Meta:
        abstract = True


class University(NameMixin, LocalIDMixin, models.Model):
    def __str__(self):
        return self.name


class Faculty(NameMixin, LocalIDMixin, models.Model):
    university = models.ForeignKey(University, related_name='faculties')

    def save(self, *args, **kwargs):
        if self.id is None:
            self.name = self.name or self.local_id or 'Faculty %s' % random.randint(10000)
        return super(Faculty, self).save(*args, **kwargs)

    def __str__(self):
        return '%s' % self.name


class Group(NameMixin, LocalIDMixin, models.Model):
    faculty = models.ForeignKey(Faculty, related_name='groups')

    def __str__(self):
        return '%s' % self.name


class LessonTime(models.Model):
    university = models.ForeignKey(University, related_name='lessons_periods')
    beginning_at = models.TimeField()
    ended_at = models.TimeField()

    def __str__(self):
        return '%s - %s' % (self.beginning_at, self.ended_at)


class LessonDate(models.Model):
    date = models.DateField()
    group = models.ForeignKey(Group)

    def __str__(self):
        return '%s' % self.date


class LessonName(NameMixin, LocalIDMixin, models.Model):
    university = models.ForeignKey(University, related_name='lessons_names')

    def __str__(self):
        return self.name


class Teacher(LocalIDMixin, models.Model):
    full_name = models.CharField(max_length=256, null=False)
    university = models.ForeignKey(University, related_name='teachers')

    def __str__(self):
        return self.full_name


class Lesson(models.Model):
    TYPE_LECTURE = 1
    TYPE_PRACTICAL_LESSON = 2
    TYPE_COLLOQUIUM = 3
    TYPE_SEMINAR = 4
    TYPE_LABORATORY_CLASS = 5
    type_choices = (
        (TYPE_LECTURE, 'Lecture'),
        (TYPE_PRACTICAL_LESSON, 'Practical lesson'),
        (TYPE_COLLOQUIUM, 'Colloquium'),
        (TYPE_SEMINAR, 'Seminar'),
        (TYPE_LABORATORY_CLASS, 'Laboratory work'),
    )

    group = models.ForeignKey(Group, related_name='lessons', null=True)
    name = models.ForeignKey(LessonName, related_name='lessons')
    type = models.PositiveSmallIntegerField(choices=type_choices)
    note = models.CharField(max_length=256, null=True)
    date = models.ForeignKey(LessonDate, related_name='lessons')
    time = models.ForeignKey(LessonTime, related_name='lessons')
    teacher = models.ForeignKey(Teacher, related_name='lessons', null=True)
    location = models.CharField(max_length=32, null=True)

    class Meta:
        ordering = ('time__beginning_at', )

    def __str__(self):
        return '[%s %s] %s (%s)' % (self.date.date, self.time, self.name, self.get_type_display())

