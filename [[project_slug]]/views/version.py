from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView


class VersionView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    @method_decorator(cache_page(60 * 60 * 24))
    def get(self, request, *args, **kwargs) -> Response:  # noqa: ARG002 ANN001 ANN002 ANN003
        return Response({'version': settings.VERSION})
