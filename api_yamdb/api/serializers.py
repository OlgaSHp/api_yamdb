from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from reviews.models import Category, Comment, Genre, Review, Title, User


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = [
            'id', 'password', 'last_login', 'is_superuser', 'is_staff',
            'is_active', 'date_joined', 'confirmation_code',
            'groups', 'user_permissions'
        ]


class UserNotAdminSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        exclude = [
            'id', 'password', 'last_login', 'is_superuser', 'is_staff',
            'is_active', 'date_joined', 'confirmation_code',
            'groups', 'user_permissions'
        ]
        read_only_fields = ("role",)


class TokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ("username", "confirmation_code")


class SignUpSerializer(serializers.ModelSerializer):
    def to_internal_value(self, data):
        email = data.get("email")
        username = data.get("username")

        user = User.objects.filter(email=email, username=username).first()
        if user:
            return user

        return super().to_internal_value(data)

    class Meta:
        model = User
        fields = ("email", "username")


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        lookup_field = "slug"
        fields = ("name", "slug")


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        lookup_field = "slug"
        fields = ("name", "slug")


class ReadOnlyTitleSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = "__all__"
        read_only_fields = (
            "id",
            "name",
            "year",
            "description",
            "category",
            "genre",
        )


class TitleSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(), slug_field="slug"
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(), many=True, slug_field="slug"
    )

    class Meta:
        model = Title
        fields = "__all__"


class ReviewSerializer(serializers.ModelSerializer):
    title = serializers.SlugRelatedField(slug_field="name", read_only=True)
    author = serializers.SlugRelatedField(
        slug_field="username", read_only=True
    )

    def validate(self, data):
        request = self.context["request"]
        author = request.user
        title_id = self.context.get("view").kwargs.get("title_id")
        title = get_object_or_404(Title, pk=title_id)
        if (
            request.method == "POST"
            and Review.objects.filter(title=title, author=author).exists()
        ):
            raise ValidationError("Разрешен только один отзыв!")
        return data

    class Meta:
        fields = "__all__"
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    review = serializers.SlugRelatedField(slug_field="text", read_only=True)
    author = serializers.SlugRelatedField(
        slug_field="username", read_only=True
    )

    class Meta:
        fields = "__all__"
        model = Comment
