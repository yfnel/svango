from django.core.management.base import BaseCommand

from actors.models import UserPermission
from actors.tests import factories


class Command(BaseCommand):

    def add_arguments(self, parser):  # noqa: ANN001 ANN201
        parser.add_argument('-s', '--superuser', type=str, dest='superuser', required=False)

    def handle(self, *args, **options):  # noqa: ARG002 ANN002 ANN003 ANN201
        superuser = options['superuser']
        if superuser:
            factories.UserFactory(
                first_name='Super', last_name='User',
                username=superuser, is_superuser=True, is_staff=True, password=superuser)
        admins = factories.GroupFactory(name='Administrators')
        admins.permissions.add(*UserPermission.objects.only('id'))
        factories.UserGroupFactory.create_batch(5, group=admins)

        managers = factories.GroupFactory(name='Managers')
        managers.permissions.add(*UserPermission.objects.filter(codename__contains='user').only('id'))
        managers.permissions.add(*UserPermission.objects.filter(codename__contains='group').only('id'))
        managers.permissions.add(*UserPermission.objects.filter(codename__startswith='view_').only('id'))
        factories.UserGroupFactory.create_batch(5, group=managers)

        users = factories.GroupFactory(name='Users')
        users.permissions.add(*UserPermission.objects.filter(codename__startswith='view_').only('id'))
        factories.UserGroupFactory.create_batch(5, group=users)

        self.stdout.write(self.style.SUCCESS('SUCCESS'))
