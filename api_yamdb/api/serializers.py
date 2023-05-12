from rest_framework import serializers

from rest_framework.validators import UniqueValidator
from django.core.validators import MaxLengthValidator

from .validators import UsernameValidator
from reviews.models import Category, Comment, Genre, Review, Title, User
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from reviews.models import Comment, Review, Title


class ReviewSerializer(serializers.ModelSerializer):
    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True
    )
    athor = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )


    class Meta:
        fields = '__all__'
        model = Review

    def validate_score(self, value):
        if 0 > value > 10:
            raise serializers.ValidationError('Оценка по 10-бальной шкале!')
        return value    

    def validate(self, data):
        request = self.context['request']
        author = request.user
        title_id = self.context.get('view').kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if (
            request.method == 'POST'
            and Review.objects.filter(title=title, author=author).exists()
        ):
            raise ValidationError('Может существовать только один отзыв!')
        return data


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class TitleSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='category')
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        many=True,
        slug_field='genre')

    class Meta:
        model = Title
        fields = '__all__'

# Или так:

# class TitleSerializer(serializers.ModelSerializer):
#     category = CategorySerializer()
#     genre = GenreSerializer(many=True)

#     class Meta:
#         model = Title
#         fields = '__all__'


class ReadOnlyTitleSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    genre = serializers.StringRelatedField(many=True)

    class Meta:
        model = Title
        fields = '__all__'
        read_only_fields = ('id', 'name', 'year',
                            'description', 'category', 'genre')


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        validators=[
            UsernameValidator(),
            MaxLengthValidator(150),
            UniqueValidator(queryset=User.objects.all())
        ],
        required=True,
    )
    email = serializers.EmailField(
        validators=[
            MaxLengthValidator(254),
            UniqueValidator(queryset=User.objects.all())
        ]
    )

    class Meta:
        fields = "__all__"
        model = User


class UserEditSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        validators=[UsernameValidator()],
        max_length=150,
        required=True
    )

    class Meta:
        fields = "__all__"
        model = User
        read_only_fields = ('role',)


class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        validators=[
            UsernameValidator(),
            MaxLengthValidator(150),
            UniqueValidator(queryset=User.objects.all())
        ]
    )
    email = serializers.EmailField(
        validators=[
            MaxLengthValidator(254),
            UniqueValidator(queryset=User.objects.all())
        ]
    )

    def validate_username(self, value):
        if value.lower() == "me":
            raise serializers.ValidationError("Пользователь с именем 'me' не разрешен")
        return value

    class Meta:
        fields = ("username", "email")
        model = User



class TokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()


class CommentSerializer(serializers.ModelSerializer):
    review = serializers.SlugRelatedField(
        slug_field='text',
        read_only=True
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        fields = '__all__'
        model = Comment
