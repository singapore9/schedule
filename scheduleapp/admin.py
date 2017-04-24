from django.contrib import admin

from .models import University, LessonTime, LessonName, Lesson, Faculty, Group, Teacher


@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    list_display = ('name', )


@admin.register(LessonTime)
class LessonTimeAdmin(admin.ModelAdmin):
    list_display = ('university', 'beginning_at', 'ended_at', )


@admin.register(LessonName)
class LessonNameAdmin(admin.ModelAdmin):
    list_display = ('university', 'name', )


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('university', 'full_name', )


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('time', 'date', 'name', 'type', 'teacher', 'note', )


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('faculty', 'name', )


@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ('university', 'name', )
