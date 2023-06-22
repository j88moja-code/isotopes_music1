from rest_framework import viewsets, serializers, mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from .serializers import TrackSerializer
from .models import Track
from users.auntentication import JWTAuthentication
from core.pagination import CustomPagination
from core.permissions import IsOwnerOrReadOnly, CustomUpdatePermission
from users.permissions import ViewPermissions, hasSelfVotedOrReadOnly


