from django.contrib.auth.models import AbstractUser
from django.db.models import Q

from django.db import models


class User(AbstractUser):
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'
    ROLES = [
        (ADMIN, 'Administrator'),
        (MODERATOR, 'Moderator'),
        (USER, 'User'),
    ]
    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        unique=True,
    )
    username = models.CharField(
        verbose_name='Имя пользователя',
        max_length=50,
        null=True,
        unique=True
    )
    role = models.CharField(
        verbose_name='Роль',
        max_length=20,
        choices=ROLES,
        default=USER
    )
    bio = models.TextField(
        verbose_name='Кто вы',
        null=True,
        blank=True
    )

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        ordering = ['id']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

        constraints = [
            models.CheckConstraint(
                check=~Q(username__iexact='me'),
                name="Имя пользователя не может быть 'me'"
            )
        ]


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=256)
    year = models.IntegerField()
    description = models.TextField()
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, related_name='titles')
    genre = models.ManyToManyField(
        Genre, through='GenreTitle')

    class Meta:
        ordering = ('name',)
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Жанр произведения'

    def __str__(self):
        return f'{self.title}, жанр - {self.genre}'


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='произведение'
    )
    text = models.CharField(max_length=200)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='автор'
    )

    score = models.IntegerField()

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return self.text


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='coments',
        verbose_name='отзыв'
    )
    text = models.CharField(
        'техт коментария',
        max_length=200

    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='coments',
        verbose_name='автор'
    )

    class Meta:
        verbose_name = 'Коментарий'
        verbose_name_plural = 'Коментарий'

    def __str__(self):
        return self.text
