from typing import Self

from django.contrib.auth.models import GroupManager as BaseGroupManager
from django.contrib.auth.models import PermissionManager
from django.contrib.auth.models import UserManager as BaseManager
from django.db.models import F, OuterRef, QuerySet


class UserQuerySet(QuerySet):

    def add_proxy_group_id(self, group_ids: list[int]) -> Self:
        sq = self.model.groups.through.objects.filter(user=OuterRef('pk'), group_id__in=group_ids)
        return self.annotate(proxy_group_id=sq.values('pk')[:1])


class UserManager(BaseManager):

    def get_queryset(self) -> UserQuerySet:
        return UserQuerySet(self.model)


class UserPermissionManager(PermissionManager):

    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter(content_type__app_label='actors').exclude(codename__endswith='permission')


class UserGroupQuerySet(QuerySet):

    def as_user(self) -> Self:
        return self.annotate(
            first_name=F('user__first_name'),
            last_name=F('user__last_name'),
            email=F('user__email'),
            username=F('user__username'),
            date_joined=F('user__date_joined'),
            is_staff=F('user__is_staff'),
            is_active=F('user__is_active'),
        )

    def as_group(self) -> Self:
        return self.annotate(name=F('group__name'))


class UserGroupManager(BaseManager):

    def get_queryset(self) -> UserGroupQuerySet:
        return UserGroupQuerySet(self.model)


class GroupQuerySet(QuerySet):

    def add_proxy_user_id(self, user_ids: list[int]) -> Self:
        sq = self.model.user_set.through.objects.filter(group=OuterRef('pk'), user_id__in=user_ids)
        return self.annotate(proxy_user_id=sq.values('pk')[:1])


class GroupManager(BaseGroupManager):

    def get_queryset(self) -> GroupQuerySet:
        return GroupQuerySet(self.model)
