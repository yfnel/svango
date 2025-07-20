from django.db.models import QuerySet
from drf_spectacular.utils import extend_schema
from rest_framework import response, viewsets

import actors.views.serializers.groups
from actors.models import PermissionGroup, User, UserGroup
from svango.utils.mixins import BulkCreateModelMixin, RelationMixin

from .serializers import groups


class GroupViewSet(viewsets.ModelViewSet):
    filterset_fields = '__all__'
    serializer_class = groups.GroupSerializer
    queryset = PermissionGroup.objects.all()


class UserGroupsViewSet(RelationMixin):
    parent_queryset = User.objects.all()
    serializer_class = groups.UserGroupsSerializer
    relation_lookup = 'groups'

    def get_queryset(self) -> QuerySet:
        user_id = self.kwargs.get('parent')
        return PermissionGroup.objects.filter(user=user_id).add_proxy_user_id([user_id])

    @extend_schema(request=groups.UserGroupsSerializer(many=False))
    def create(self, request, *args, **kwargs) -> response.Response: # noqa: ANN001, ANN002, ANN003
        return super().create(request, *args, **kwargs)


class UserGroupViewSet(viewsets.ModelViewSet, BulkCreateModelMixin):
    queryset = UserGroup.objects.select_related('user', 'group').all()
    serializer_class = actors.views.serializers.groups.UserGroupSerializer
