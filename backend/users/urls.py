from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import (
    RegisterAPIView, login, AuthenticatedUser, logout,
    RoleViewSet, UserGenericAPIView, ProfileInfoAPIView,
    ProfilePasswordAPIView, ProfileImageUploadView, FollowUser
)

urlpatterns = [
    path('register', RegisterAPIView.as_view()),
    path('login', login),
    path('user', AuthenticatedUser.as_view()),
    path('logout', logout),
    path('roles', RoleViewSet.as_view({
        'get': 'list'
    })),
    path('roles/<str:pk>', RoleViewSet.as_view({
        'get': 'retrieve'
    })),
    path('users/info', ProfileInfoAPIView.as_view()),
    path('users/password', ProfilePasswordAPIView.as_view()),
    path('users', UserGenericAPIView.as_view()),
    path('profile_pic_upload', ProfileImageUploadView.as_view()),

    path('user/follow/<str:pk>', FollowUser.as_view()),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)