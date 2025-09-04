from django.conf import settings
from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from actors.views import groups, users

router = DefaultRouter()
if 'rest_framework.authentication.SessionAuthentication' in settings.REST_FRAMEWORK.DEFAULT_AUTHENTICATION_CLASSES:
    router.register('users/login', users.UserLoginViewSet, basename='users-login')
router.register('users', users.UserViewSet, basename='users')
router.register('users/(?P<parent>[0-9]+)/groups', groups.UserGroupsViewSet, basename='user-groups')
router.register('groups', groups.GroupViewSet, basename='groups')
router.register('groups/(?P<parent>[0-9]+)/users', users.GroupUsersViewSet, basename='group-users')
router.register('user-group', groups.UserGroupViewSet, basename='user-group')

urlpatterns = [
    path('token-obtain/', TokenObtainPairView.as_view(), name='token-obtain'),
    path('token-refresh/', TokenRefreshView.as_view(), name='token-refresh'),
]
urlpatterns.extend(router.urls)
