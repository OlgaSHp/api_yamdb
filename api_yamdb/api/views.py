from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination


from reviews.models import Category, Genre, Review, Title, User
from .filters import TitleFilter
from .mixins import ListCreateDestroyViewSet
from .permissions import (IsAdmin, IsAdminOrReadOnly,
                          IsAdminModeratorOwnerOrReadOnly)
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReadOnlyTitleSerializer,
                          RegisterDataSerializer, ReviewSerializer,
                          TitleSerializer, TokenSerializer, UserEditSerializer,
                          UserSerializer)


class CategoryViewSet(ListCreateDestroyViewSet):
    '''Получить список всех категорий.'''
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (SearchFilter, )
    search_fields = ('name', )
    lookup_field = 'slug'


class GenreViewSet(ListCreateDestroyViewSet):
    '''Получить список всех жанров.'''
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ('name', )
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    '''Вьюсет получения, записи и изменения произведений.'''
    queryset = Title.objects.all()
    filter_backends = (DjangoFilterBackend, )
    filterset_class = TitleFilter
    permission_classes = (IsAdminOrReadOnly,)

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return ReadOnlyTitleSerializer
        return TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    pass


class CommentViewSet(viewsets.ModelViewSet):
    pass
