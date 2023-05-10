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

    


class UserViewSet(viewsets.ModelViewSet):
    pass

# @api_view(["POST"])
# @permission_classes([permissions.AllowAny])
# def register_user(request):
# ''' Регистрируем нового пользователя'''


# @api_view(["POST"])
# @permission_classes([permissions.AllowAny])
# def get_jwt_token(request):
#     '''Запрашиваем токен'''


class ReviewViewSet(viewsets.ModelViewSet):
    pass


class CommentViewSet(viewsets.ModelViewSet):
    pass