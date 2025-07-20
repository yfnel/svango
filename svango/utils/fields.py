from django.db import models
from rest_framework import serializers


class RelationField(serializers.PrimaryKeyRelatedField):

    def get_queryset(self) -> models.QuerySet:
        return self.root.Meta.model.objects.all()
