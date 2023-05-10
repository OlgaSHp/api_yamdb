from django.contrib.auth.models import AbstractUser

from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model):
    name = 
    slug = 


class Genre(models.Model):
    name = 
    slug = 


class Title(models.Model):
    name = 
    year = 
    category_id = 


class GenreTitle(models.Model):
    pass


class Review(models.Model):
    pass


class Comment(models.Model):
    pass
