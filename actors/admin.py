from django.contrib import admin
from django.contrib.auth.models import Group

from . import models

admin.site.unregister(Group)

class UserGroupInline(admin.StackedInline):
    model = models.UserGroup


class UserInline(admin.StackedInline):
    model = models.UserGroup


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    inlines = (UserGroupInline,)
    list_display = ('first_name', 'last_name', 'username', 'email', 'is_staff', 'is_active', 'photo')
    exclude = ('user_permissions', 'groups')


@admin.register(models.PermissionGroup)
class PermissionGroupAdmin(admin.ModelAdmin):
    inlines = (UserInline,)
    list_display = ('name',)
    exclude = ('permissions',)

