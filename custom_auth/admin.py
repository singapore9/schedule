from django.contrib import admin

from .models import Token, ApplicationUser


@admin.register(Token)
class VkTokenAdmin(admin.ModelAdmin):
    list_display = ('token', 'user', 'created_at', 'expires_in', )


@admin.register(ApplicationUser)
class ApplicationUserAdmin(admin.ModelAdmin):
    list_display = ('email', )
