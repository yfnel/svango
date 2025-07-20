from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

from . import managers


class User(AbstractUser):
    photo = models.ImageField(null=True, blank=True)

    objects = managers.UserManager()

    def __str__(self) -> str:
        return self.get_full_name()


class UserPermission(Permission):
    objects = managers.UserPermissionManager()

    class Meta:
        proxy = True


class PermissionGroup(Group):
    objects = managers.GroupManager()

    class Meta:
        proxy = True


class UserGroup(User.groups.through):
    objects = managers.UserGroupManager()

    class Meta:
        proxy = True

    def __str__(self) -> str:
        return f'{self.pk} {self.user_id} {self.group_id}'


class GroupPermission(Group.permissions.through):

    class Meta:
        proxy = True

    def __str__(self) -> str:
        return f'{self.pk} {self.permission_id} {self.group_id}'
