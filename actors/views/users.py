from django.contrib.auth import login
from django.db.models import QuerySet
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.debug import sensitive_post_parameters
from django_filters import rest_framework as drf_filters
from drf_spectacular.utils import extend_schema
from rest_framework import permissions, serializers, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from actors.models import PermissionGroup, User
from common.utils.mixins import RelationMixin

from .serializers import users

sensitive_post_parameters_m = method_decorator(sensitive_post_parameters('password'))


class UserFilterSet(drf_filters.FilterSet):
    id = drf_filters.BaseInFilter(field_name='id', lookup_expr='in')

    class Meta:
        model = User
        fields = '__all__'
        exclude = ('photo', 'password', 'is_superuser', 'user_permissions')


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    filterset_class = UserFilterSet
    ordering_fields = sorted(UserFilterSet.get_fields())
    search_fields = ('username', 'first_name', 'last_name', 'email')

    def get_object(self) -> User:
        if self.action in ('me', 'my_password'):
            return self.request.user
        return super().get_object()

    def get_serializer_class(self) -> type[users.UserPasswordSerializer | users.UserSerializer]:
        if self.action == 'my_password':
            return users.UserPasswordSerializer
        return users.UserSerializer

    @action(methods=('GET',), url_path='me', detail=False, permission_classes=[permissions.IsAuthenticated])
    def me(self, request, *args, **kwargs) -> Response:  # noqa: ANN001 ANN002 ANN003
        return self.retrieve(request, *args, **kwargs)

    @action(
        methods=('PUT',), url_path='my-password', detail=False, permission_classes=[permissions.IsAuthenticated],
    )
    def my_password(self, request, *args, **kwargs) -> Response:  # noqa: ANN001 ANN002 ANN003
        return self.update(request, *args, **kwargs)


class UserLoginViewSet(viewsets.ModelViewSet):
    http_method_names = ('post',)
    permission_classes = (permissions.AllowAny,)
    serializer_class = users.UserLoginSerializer

    @sensitive_post_parameters_m
    @method_decorator(never_cache)
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):  # noqa: ANN002 ANN003 ANN201
        return super().dispatch(*args, **kwargs)

    def perform_create(self, serializer: serializers.Serializer) -> None:
        user = serializer.validated_data['user']
        login(self.request, user)
        super().perform_create(serializer)


class GroupUsersViewSet(RelationMixin):
    parent_queryset = PermissionGroup.objects.all()
    serializer_class = users.GroupUsersSerializer
    relation_lookup = 'user_set'

    def get_queryset(self) -> QuerySet:
        group_id = self.kwargs.get('parent')
        return User.objects.all().filter(groups=group_id)

    @extend_schema(request=users.GroupUsersSerializer(many=False))
    def create(self, request, *args, **kwargs) -> Response: # noqa: ANN001, ANN002, ANN003
        return super().create(request, *args, **kwargs)
