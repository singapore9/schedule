from django.contrib import admin

from .models import ApplicationUser


@admin.register(ApplicationUser)
class ApplicationUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'id')
