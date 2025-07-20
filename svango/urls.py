from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

API_ROOT = 'api/v1/'


urlpatterns = [
    path(r'admin/', admin.site.urls),
    path(rf'{API_ROOT}actors/', include('actors.urls')),
    path(f'{API_ROOT}schema/', SpectacularAPIView.as_view(), name='schema'),
    path(f'{API_ROOT}schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path(f'{API_ROOT}schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

if settings.DEBUG and settings.ENV_FOR_DYNACONF == 'DEVELOPMENT':  # pragma: no cover
    urlpatterns.extend(static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))
    urlpatterns.extend(static(settings.STATIC_URL, document_root=settings.STATIC_ROOT))
