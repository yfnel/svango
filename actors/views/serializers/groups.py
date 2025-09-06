from django.contrib.auth.models import Group
from rest_framework import serializers

from actors.models import PermissionGroup, UserGroup
from actors.views.serializers.users import UserSerializer
from common.utils.fields import RelationField


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        exclude = ('permissions',)


class UserGroupsSerializer(GroupSerializer):
    relations = RelationField(many=True, required=True, write_only=True)

    class Meta(GroupSerializer.Meta):
        model = PermissionGroup
        read_only_fields = ('id', 'name', 'permissions')


class UserGroupSerializer(serializers.ModelSerializer):
    user_data = UserSerializer(source='user', read_only=True)
    group_data = GroupSerializer(source='group', read_only=True)

    class Meta:
        model = UserGroup
        fields = '__all__'
