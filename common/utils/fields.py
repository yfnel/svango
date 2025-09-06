from django.db import models
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers


@extend_schema_field(OpenApiTypes.INT)
class RelationField(serializers.PrimaryKeyRelatedField):

    def get_queryset(self) -> models.QuerySet:
        return self.root.Meta.model.objects.all()
