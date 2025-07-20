from collections.abc import Iterable

from django.db import models
from django.utils.functional import cached_property
from rest_framework import generics, response, serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin


class BulkCreateModelMixin(CreateModelMixin):
    """Create model instances in bulk."""

    def get_serializer(self, *args, **kwargs) -> serializers.Serializer:  # noqa: ANN002, ANN003
        if self.action == 'bulk_create':
            kwargs['many'] = True
        return super().get_serializer(*args, **kwargs)

    @action(methods=('POST',), url_path='bulk-create', detail=False)
    def bulk_create(self, request, *args, **kwargs) -> response.Response:  # noqa: ANN001 ANN002 ANN003
        return self.create(request, *args, **kwargs)


class RelationMixin(viewsets.ModelViewSet):
    parent_kwarg = 'parent'
    parent_queryset = None
    relation_lookup = None

    @cached_property
    def is_swagger(self) -> bool:
        return getattr(self, 'swagger_fake_view', False)

    @cached_property
    def parent(self) -> models.Model | None:
        if self.is_swagger:  # pragma: no cover
            return None
        return generics.get_object_or_404(self.get_parent_queryset(), pk=self.kwargs[self.parent_kwarg])

    def get_parent_queryset(self, *args, **kwargs) -> models.QuerySet:  # noqa: ARG002 ANN002  ANN003
        return self.parent_queryset

    def get_serializer_context(self) -> dict:
        ctx = super().get_serializer_context()
        ctx['parent'] = self.parent
        return ctx

    def get_serializer(self, *args, **kwargs) -> serializers.Serializer:  # noqa: ANN002, ANN003
        if self.is_swagger and self.action == 'create':  # pragma: no cover
            self.pagination_class = None
            kwargs['many'] = True
        return super().get_serializer(*args, **kwargs)

    def change_relations(self, relations: Iterable[models.Model]) -> None:
        manager = getattr(self.parent, self.relation_lookup)
        (manager.remove, manager.add)[self.action == 'create'](*relations)

    def perform_destroy(self, instance: models.Model) -> None:
        """Delete only m2m table record, not the record itself."""
        self.change_relations([instance])

    def create(self, request, *args, **kwargs) -> response.Response: # noqa: ARG002 ANN001 ANN002 ANN003
        """Create m2m table records."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        relations = serializer.validated_data['relations']
        self.change_relations(relations)
        headers = self.get_success_headers(serializer.data)
        data = self.get_serializer(instance=relations, many=True).data
        return response.Response(data, status=status.HTTP_201_CREATED, headers=headers)

    @action(methods=('PATCH',), url_path='unlink', detail=False)
    def unlink(self, request, *args, **kwargs) -> response.Response:  # noqa: ARG002 ANN001 ANN002 ANN003
        """Delete only m2m table records."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.change_relations(serializer.validated_data['relations'])
        return response.Response(status=status.HTTP_204_NO_CONTENT)
