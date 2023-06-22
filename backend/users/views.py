from rest_framework import exceptions, viewsets, generics, mixins, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.parsers import MultiPartParser
from django.core.exceptions import ObjectDoesNotExist

from django.core.files.storage import default_storage
from django.shortcuts import get_object_or_404

from .models import User, Role, UserFollow
from .serializers import UserFollowSerializer, UserSerializer, RoleSerializer
from .auntentication import generate_access_token, JWTAuthentication
from core.pagination import CustomPagination
from .permissions import ViewPermissions, hasSelfVotedOrReadOnly

class RegisterAPIView(APIView):
    def post(self, request):
        data = request.data

        if data['password'] != data['confirm_password']:
            raise exceptions.APIException('Passwords do not match!')

        request.data.update({
        'role': request.data['role_id']
        })
        serializer = UserSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

@api_view(['POST'])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    user = User.objects.filter(email=email).first()

    if user is None:
        raise exceptions.AuthenticationFailed('User not found!')
    
    if not user.check_password(password):
        raise exceptions.AuthenticationFailed('Incorrect password')
    
    response = Response()

    token = generate_access_token(user)
    response.set_cookie(key='jwt', value=token, httponly=True)
    response.data = {
        'jwt': token
    }

    return response

@api_view(['POST'])
def logout(_):
    response = Response()
    response.delete_cookie(key='jwt')
    response.data = {
        'message': 'Successfully logged out'
    }

    return response

class AuthenticatedUser(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        data = UserSerializer(request.user).data
        data['permissions'] = [p['name'] for p in data['role']['permissions']]

        return Response({
            'data': data
        })

class RoleViewSet(viewsets.ViewSet):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticatedOrReadOnly]

    def list(self, request):
        serializer = RoleSerializer(Role.objects.all(), many=True)

        return Response({
            'data': serializer.data
        })

    def retrieve(self, request, pk=None):
        role = Role.objects.get(id=pk)
        serializer =  RoleSerializer(role)

        return Response({
            'data': serializer.data
        })
    
class UserGenericAPIView(
    generics.GenericAPIView, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin,
    mixins.UpdateModelMixin, mixins.DestroyModelMixin
):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated & ViewPermissions]
    permission_object = 'users'
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = CustomPagination

    def get(self, request, pk=None):
        if pk:
            return Response({
                'data': self.retrieve(request, pk).data
            })

        return self.list(request)

# class ProfileViewSet(viewsets.ViewSet):
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,
#                           CustomUpdatePermission]

#     # def perform_create(self, serializer):
#     #     serializer.save(owner=self.request.user)
#     def list(self, request):
#         serializer = ProfileSerializer(UserProfile.objects.all(), many=True)

#         return Response({
#             'data': serializer.data
#         })
       
#     def create(self, request):
#         serializer = ProfileSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save(owner=self.request.user)
#         return Response({
#             'data': serializer.data
#         }, status=status.HTTP_201_CREATED)

#     def retrieve(self, request, pk=None):
#         profile_data = UserProfile.objects.get(id=pk)
#         serializer = ProfileSerializer(profile_data)

#         return Response({
#             'data': serializer.data
#         })

#     def update(self, request, pk=None):
#         queryset = UserProfile.objects.all()
#         profile_data = get_object_or_404(queryset, pk=pk)
#         serializer = ProfileSerializer(instance=profile_data, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()

#         return Response({
#             'data': serializer.data
#         }, status=status.HTTP_202_ACCEPTED)

#     def destroy(self, request, pk=None):
#         queryset = UserProfile.objects.all()
#         profile_data = get_object_or_404(queryset, pk=pk)
#         profile_data.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

    
class ProfileInfoAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request, pk=None):
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
class ProfilePasswordAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request, pk=None):
        user = request.user

        if request.data['password'] != request.data['confirm_password']:
            raise exceptions.ValidationError('Passwords do not match')

        user.set_password(request.data['password'])
        user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
class ProfileImageUploadView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser,)

    def post(self, request):
        file = request.FILES['image']
        file_name = default_storage.save(file.name, file)
        url = default_storage.url(file_name)

        return Response({
            'url': 'http://localhost:8001/api' + url,
        })
    
class FollowUser(APIView):
    queryset = UserFollow.objects.all()
    serializer_class = UserFollowSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        following = UserFollow.objects.filter(user=request.user)
        followers = UserFollow.objects.filter(follows=request.user)

        following_serializer = UserFollowSerializer(following, many=True)
        followers_serializer = UserFollowSerializer(followers, many=True)
        return Response({ "success": True, "following": following_serializer.data, "followers": followers_serializer.data })


    def post(self, request, pk):
        try:
            following_user = User.objects.get(id=pk)
            follow_user = UserFollow.objects.get_or_create(user=request.user, follows=following_user)
            if not follow_user[1]:
                follow_user[0].delete()
                return Response({ "success": True, "message": "unfollowed user" })
            else:
                return Response({ "success": True, "message": "followed user" })


        except ObjectDoesNotExist:
            return Response({ "success": False, "message": "following user does not exist" })