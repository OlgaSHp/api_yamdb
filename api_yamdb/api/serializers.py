from rest_framework import serializers

from rest_framework.validators import UniqueValidator
from django.core.validators import MaxLengthValidator

from .validators import UsernameValidator
from reviews.models import Category, Comment, Genre, Review, Title, User


class ReviewSerializer(serializers.ModelSerializer):
    pass


class CategorySerializer(serializers.ModelSerializer):
    pass


class GenreSerializer(serializers.ModelSerializer):
    pass


class TitleSerializer(serializers.ModelSerializer):
    pass


class ReadOnlyTitleSerializer(serializers.ModelSerializer):
    pass


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
    pass
