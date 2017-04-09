from django.db import models


class University(models.Model):
    name = models.CharField(max_length=100, null=False)

    def __str__(self):
        return self.name


class Faculty(models.Model):
    university = models.ForeignKey(University, related_name='faculties')
    name = models.CharField(max_length=100, null=False)

    def __str__(self):
        return 'Faculty %s' % self.name


class Group(models.Model):
    faculty = models.ForeignKey(Faculty, related_name='groups')
    name = models.CharField(max_length=100, null=False)

    def __str__(self):
        return 'Group %s' % self.name


class LessonTime(models.Model):
    university = models.ForeignKey(University, related_name='lessons_periods')
    beginning_at = models.TimeField()
    ended_at = models.TimeField()

    def __str__(self):
        return '%s - %s' % (self.beginning_at, self.ended_at)


class LessonName(models.Model):
    name = models.CharField(max_length=256, null=False)
    university = models.ForeignKey(University, related_name='lessons_names')

    def __str__(self):
        return self.name


class Teacher(models.Model):
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
    date = models.DateField()
    period = models.ForeignKey(LessonTime, related_name='lessons')
    teacher = models.ForeignKey(Teacher, related_name='lessons')

    def _type_to_str(self):
        return list(filter(lambda _tuple: _tuple[0] == self.type, self.type_choices))[0][1]

    def __str__(self):
        return '[%s %s] %s (%s)' % (self.date, self.period, self.name, self._type_to_str())
