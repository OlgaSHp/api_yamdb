from django.contrib.auth.models import AbstractUser
from django.contrib.auth.tokens import default_token_generator
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from .validators import validate_username, validate_year

USER = "user"
ADMIN = "admin"
MODERATOR = "moderator"

ROLES = [
    (USER, USER),
    (ADMIN, ADMIN),
    (MODERATOR, MODERATOR),
]


class User(AbstractUser):
    username = models.CharField(
        validators=(validate_username,),
        max_length=150,
        unique=True,
        blank=False,
        null=False,
    )
    email = models.EmailField(
        max_length=254, unique=True, blank=False, null=False
    )
    role = models.CharField(
        "Роль", max_length=20, choices=ROLES, default=USER, blank=True
    )
    bio = models.TextField(
        "Персональная информация",
        blank=True,
    )
    confirmation_code = models.CharField(
        "Код подтверждения",
        max_length=255,
        null=True,
        blank=False,
        default="XXX",
    )

    @property
    def is_user(self):
        return self.role == USER

    @property
    def is_admin(self):
        return self.role == ADMIN

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    class Meta:
        ordering = ("id",)
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.username


@receiver(post_save, sender=User)
def post_save(sender, instance, created, **kwargs):
    if created:
        confirmation_code = default_token_generator.make_token(instance)
        instance.confirmation_code = confirmation_code
        instance.save()


class Category(models.Model):
    name = models.CharField("Название категории", max_length=200)
    slug = models.SlugField("Слаг категории", unique=True, db_index=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return f"{self.name} {self.name}"


class Genre(models.Model):
    name = models.CharField("Название жанра", max_length=50)
    slug = models.SlugField("Слаг жанра", unique=True, db_index=True)

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

    def __str__(self):
        return f"{self.name} {self.name}"


class Title(models.Model):
    name = models.CharField("Название", max_length=50, db_index=True)
    year = models.IntegerField("Год", validators=(validate_year,))
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name="titles",
        verbose_name="Категория",
        null=True,
        blank=True,
    )
    description = models.TextField(
        "Описание", max_length=255, null=True, blank=True
    )
    genre = models.ManyToManyField(
        Genre, related_name="titles", verbose_name="Жанр"
    )

    class Meta:
        verbose_name = "Произведение"
        verbose_name_plural = "Произведения"

    def __str__(self):
        return self.name


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Отзыв",
    )
    text = models.CharField(max_length=200)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Автор",
    )
    score = models.IntegerField(
        "Рейтинг",
        validators=(MinValueValidator(1), MaxValueValidator(10)),
        error_messages={"validators": "Рейтинг не может быть выше 10"},
    )
    pub_date = models.DateTimeField(
        "Дата публикации", auto_now_add=True, db_index=True
    )

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        constraints = [
            models.UniqueConstraint(
                fields=(
                    "title",
                    "author",
                ),
                name="unique review",
            )
        ]
        ordering = ("pub_date",)

    def __str__(self):
        return self.text


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Комментарий",
    )
    text = models.CharField("Текст комментария", max_length=200)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Автор",
    )
    pub_date = models.DateTimeField(
        "Дата публикации", auto_now_add=True, db_index=True
    )

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    def __str__(self):
        return self.text
