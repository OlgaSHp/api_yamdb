from rest_framework import serializers

from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from reviews.models import Category, Genre, Comment, Review, Title


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
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'
        lookup_field = 'slug'


class TitleSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug')
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        many=True,
        slug_field='slug')

    class Meta:
        model = Title
        fields = '__all__'


class ReadOnlyTitleSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(
        read_only=True,
        many=True
    )

    class Meta:
        model = Title
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    pass


class UserEditSerializer(serializers.ModelSerializer):
    pass


class RegisterDataSerializer(serializers.ModelSerializer):
    pass


class TokenSerializer(serializers.Serializer):
    pass


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
