from django.contrib import admin
from .models import *


class UserAdminList(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'job_title', 'email')
    list_display_links = ('first_name', 'last_name')
    search_fields = ('first_name', 'last_name')
    readonly_fields = ('first_name', 'last_name', 'email')


class TaskAdminList(admin.ModelAdmin):
    list_display = ('title', 'text', 'user', 'date_create', 'deadline')
    list_display_links = ('title',)
    search_fields = ('title',)
    fields = ('title', 'text', 'status', 'user')
    readonly_fields = ('user',)


admin.site.register(Task, TaskAdminList)
admin.site.register(User, UserAdminList)
