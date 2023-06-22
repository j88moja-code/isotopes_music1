from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import (
    EventGenericAPIView, EventImageUploadView, VoteEventAPIView,
    CommentPost
)

urlpatterns = [
    path('events', EventGenericAPIView.as_view()),
    path('events/<str:pk>', EventGenericAPIView.as_view()),
    path('event_image_upload', EventImageUploadView.as_view()),

    path('event/vote/<str:pk>', VoteEventAPIView.as_view()),

    path('event/comment/<str:pk>', CommentPost.as_view()),
    path('event/comments/<str:pk>', CommentPost.as_view()),

] 
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)