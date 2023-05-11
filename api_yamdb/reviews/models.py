from django.contrib.auth.models import AbstractUser

from django.db import models




class User(AbstractUser):
    pass


class Category(models.Model):
    pass


class Genre(models.Model):
    pass


class Title(models.Model):
    pass


class GenreTitle(models.Model):
    pass


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


