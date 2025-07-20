from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Permission
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from actors.models import User
from svango.utils.fields import RelationField
from svango.utils.permissions import get_fields


class UserSerializer(serializers.ModelSerializer):
    has_password = serializers.BooleanField(read_only=True, source='has_usable_password')

    class Meta:
        model = User
        exclude = ('groups', 'user_permissions', 'password', 'is_superuser')
        read_only_fields = ('date_joined',)

    def create(self, validated_data: dict) -> User:
        validated_data['password'] = make_password(None)
        return super().create(validated_data)


class UserPasswordSerializer(serializers.ModelSerializer):
    current_password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('current_password', 'password')

    def validate_current_password(self, password: str) -> str:
        if not self.instance.check_password(password):
            msg = 'Current password is incorrect'
            raise serializers.ValidationError(msg)
        return password

    def validate_password(self, password: str) -> str:
        validate_password(password, self.instance)
        return make_password(password)


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ('id', 'name', 'content_type', 'codename')
        read_only_fields = fields


class UserLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True, required=True)

    class Meta:
        model = User
        exclude = ('groups', 'user_permissions', 'is_superuser')
        read_only_fields = get_fields(User,('username', 'password'))

    def validate(self, attrs):  # noqa: ANN001 ANN201
        attrs['user'] = authenticate(self.context['request'], username=attrs['username'], password=attrs['password'])
        if attrs['user'] is None:
            err_msg = 'Błędny login lub hasło'
            raise serializers.ValidationError(err_msg)
        return attrs

    def create(self, validated_data: dict) -> User:
        return validated_data['user']


class GroupUsersSerializer(serializers.ModelSerializer):
    relations = RelationField(many=True, required=True, write_only=True)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'relations')
        read_only_fields = ('id', 'first_name')
