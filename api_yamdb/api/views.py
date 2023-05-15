from django.core.mail import EmailMessage
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from api.filters import TitleFilter


from reviews.models import Category, Genre, Review, Title, User


from .filters import TitleFilter
from .mixins import ListCreateDestroyViewSet
from .permissions import (IsAdminModeratorOwnerOrReadOnly, IsAdmin,
                          IsAdminOrReadOnly)

from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, TokenSerializer,
                          UserNotAdminSerializer, ReviewSerializer,
                          SignUpSerializer,
                          UsersSerializer,
                          ReadOnlyTitleSerializer, TitleSerializer)


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    permission_classes = (IsAuthenticated, IsAdmin,)
    lookup_field = 'username'
    filter_backends = (SearchFilter, )
    search_fields = ('username', )
    http_method_names = ['get', 'post', 'patch', 'delete']

    @action(
        methods=['GET', 'PATCH'],
        detail=False,
        permission_classes=(IsAuthenticated,),
        url_path='me')
    def get_current_user_info(self, request):
        """
        Получение информации о текущем пользователе.

        Если метод запроса PATCH, то проверяется, является ли пользователь администратором.
        Если пользователь - администратор, используется сериализатор UsersSerializer для
        обновления информации о текущем пользователе на основе полученных данных.
        В противном случае используется сериализатор UserNotAdminSerializer для частичного
        обновления информации о текущем пользователе на основе полученных данных.

        Возвращает сериализированные данные о текущем пользователе или код ответа HTTP 200 OK.
        """
        serializer = UsersSerializer(request.user)
        if request.method == 'PATCH':
            if request.user.is_admin:
                serializer = UsersSerializer(
                    request.user,
                    data=request.data,
                    partial=True)
            else:
                serializer = UserNotAdminSerializer(
                    request.user,
                    data=request.data,
                    partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data)


class APIToken(APIView):
    """
    Получение JWT-токена в обмен на username и confirmation code.
    """

    def post(self, request):
        """
        Отправка запроса на получение JWT-токена.

        Проверяет наличие пользователя с указанным username.
        Если код подтверждения совпадает с кодом пользователя,
        генерирует и возвращает JWT-токен для пользователя.

        Возвращает JWT-токен или соответствующий код ответа HTTP.
        """
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        try:
            user = User.objects.get(username=data['username'])
        except User.DoesNotExist:
            return Response(
                {'username': 'Пользователь не найден'},
                status=status.HTTP_404_NOT_FOUND)
        if data.get('confirmation_code') == user.confirmation_code:
            token = RefreshToken.for_user(user).access_token
            return Response({'token': str(token)},
                            status=status.HTTP_201_CREATED)
        return Response(
            {'confirmation_code': 'Неверный код подтверждения'},
            status=status.HTTP_400_BAD_REQUEST)


class APISignup(APIView):
    """
    Получение кода подтверждения на электронную почту.
    """
    permission_classes = (permissions.AllowAny,)

    @staticmethod
    def send_email(data):
        """
        Отправка электронного письма.
        """
        email = EmailMessage(
            subject=data['email_subject'],
            body=data['email_body'],
            to=[data['to_email']]
        )
        email.send()

    def post(self, request):
        """
        Отправка запроса на получение кода подтверждения.
        """
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Проверка на существование электронной почты
        email = request.data.get('email', None)
        if email and User.objects.filter(email=email).exists():
            raise ValidationError(
                {'email': 'Такая электронная почта уже существует'})

        user = serializer.save()
        email_body = (
            f'Добрый день {user.username}.'
            f'\nВаш код для доступа к API: {user.confirmation_code}'
        )
        data = {
            'email_body': email_body,
            'to_email': user.email,
            'email_subject': 'Код подтверждения для доступа к API'
        }
        self.send_email(data)
        return Response(serializer.data, status=status.HTTP_200_OK)


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


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAdminModeratorOwnerOrReadOnly,)


    def get_queryset(self):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'))
        return review.comments.all()
    
    def perform_create(self, serializer):
        review = get_object_or_404(
            Review, 
            id = self.kwargs('review_id')
        )
        serializer.save(author=self.request.user, review=review)



class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAdminModeratorOwnerOrReadOnly,)


    def get_queryset(self):
        title = get_object_or_404(
            Title,
            id = self.kwargs('title_id')
        )
        return title.reviews.all()
    

    def perform_create(self, serializer):
        title = get_object_or_404(
            Title,
            id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)
