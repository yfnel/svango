import factory.fuzzy
from django.contrib.auth.models import Permission

from actors import models
from actors.models import GroupPermission, PermissionGroup, UserGroup


class ModelFactory(factory.django.DjangoModelFactory):

    @classmethod
    def as_dict(cls, _skip_empty=None, **kwargs) -> dict:  # noqa: ANN001 ANN003
        return factory.build(dict, **kwargs, FACTORY_CLASS=cls)


class UserFactory(ModelFactory):
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.lazy_attribute(lambda o: f'{o.first_name}.{o.last_name}@svango.com'.lower())
    username = factory.SelfAttribute('.email')
    password = factory.django.Password('pwd')

    class Meta:
        model = models.User


class GroupFactory(ModelFactory):
    name = factory.Faker('company')

    class Meta:
        model = PermissionGroup


class UserGroupFactory(ModelFactory):
    user = factory.SubFactory(UserFactory)
    group = factory.SubFactory(GroupFactory)

    class Meta:
        model = UserGroup


class GroupPermissionFactory(ModelFactory):
    permission = factory.Iterator(Permission.objects.all())
    group = factory.SubFactory(GroupFactory)

    class Meta:
        model = GroupPermission
