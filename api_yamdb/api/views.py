from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes


from reviews.models import Category, Genre, Review, Title, User
from .mixins import ListCreateDestroyViewSet
from .permissions import (IsAdmin, IsAdminOrReadOnly,
                          IsAdminModeratorOwnerOrReadOnly)
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReadOnlyTitleSerializer,
                          RegisterDataSerializer, ReviewSerializer,
                          TitleSerializer, TokenSerializer, UserEditSerializer,
                          UserSerializer)

class CategoryViewSet(ListCreateDestroyViewSet):
    pass


class GenreViewSet(ListCreateDestroyViewSet):
    pass


class TitleViewSet(viewsets.ModelViewSet):
    pass

 
class ReviewViewSet(viewsets.ModelViewSet):
    pass


class CommentViewSet(viewsets.ModelViewSet):
    pass