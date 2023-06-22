from rest_framework import serializers, viewsets, generics, mixins, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.parsers import MultiPartParser
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.storage import default_storage

from .serializers import EventSerializer, VoteEventSerializer, CommentSerializer
from .models import Event, VoteEvent, EventComment

from users.auntentication import JWTAuthentication
from core.pagination import CustomPagination
from core.permissions import IsOwnerOrReadOnly, CustomUpdatePermission
from users.permissions import ViewPermissions, hasSelfVotedOrReadOnly
   
class EventGenericAPIView(
    generics.GenericAPIView, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin,
    mixins.UpdateModelMixin, mixins.DestroyModelMixin
):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly & ViewPermissions]
    permission_object = 'events'
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    pagination_class = CustomPagination

    def get(self, request, pk=None):
        if pk:
            return Response({
                'data': self.retrieve(request, pk).data
            })

        return self.list(request)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        response = self.partial_update(request)
        return response

    def delete(self, request, pk=None):
        return self.destroy(request, pk)

class EventImageUploadView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly & ViewPermissions]
    permission_object = 'events'
    parser_classes = (MultiPartParser,)

    def post(self, request):
        file = request.FILES['image']
        file_name = default_storage.save(file.name, file)
        url = default_storage.url(file_name)

        return Response({
            'url': 'http://localhost:8001/api' + url
        })
    
class VoteEventAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes=[IsAuthenticatedOrReadOnly,hasSelfVotedOrReadOnly]
    serializer_class=EventSerializer
    
    def get(self, request, pk):
        try:
            event = Event.objects.get(id=pk)
            likes_list = VoteEvent.objects.filter(event=event)

            serializer = VoteEventSerializer(likes_list, many=True)
            return Response({ "success": True, "likes_list": serializer.data })

        except ObjectDoesNotExist:
            return Response({ "success": False, "message": "event does not exist" })

    def post(self, request, pk):
        try:
            event = Event.objects.get(id=pk)
            new_event_like = VoteEvent.objects.get_or_create(user=request.user, event=event)
            if not new_event_like[1]:
                new_event_like[0].delete()
                return Response({ "success": True, "message": "event unliked" })
            else:
                return Response({ "success": True, "message": "event liked" })

        except ObjectDoesNotExist:
            return Response({ "success": False, "message": "event does not exist" })

class CommentPost(generics.CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    queryset = EventComment.objects.all()
    serializer_class = CommentSerializer

    def get(self, request, pk):
        try:
            context = {
                "request": request,
            }
            event = Event.objects.get(id=pk)
            comments = EventComment.objects.filter(event=event)
            serializer = self.serializer_class(comments, many=True)
            return Response({ "success": True, "comments": serializer.data })


        except ObjectDoesNotExist:
            return Response({ "success": False, "message": "post does not exist" })

    def post(self, request, pk):
        try:
            context = {
                "request": request,
            }
            event = Event.objects.get(id=pk)
            
            serializer = self.serializer_class(context=context, data=request.data)
            if serializer.is_valid():
                serializer.save(event=event)
                return Response({ "success": True, "message": "comment added" })
            else:
                print(serializer.errors)
                return Response({ "success": False, "message": "error adding a comment" })


        except ObjectDoesNotExist:
            return Response({ "success": False, "message": "post does not exist" })