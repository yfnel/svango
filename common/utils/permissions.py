from collections.abc import Iterable

from django.db import models
from rest_framework.permissions import DjangoModelPermissions


class DjangoModelCrudPermissions(DjangoModelPermissions):
    DjangoModelPermissions.perms_map['GET'].append('%(app_label)s.view_%(model_name)s')


def get_fields(model: type[models.Model], omit: Iterable[str]=()) -> list[str]:
    return [f.name for f in model._meta.fields if f.concrete and f.name not in omit]  # noqa: SLF001
