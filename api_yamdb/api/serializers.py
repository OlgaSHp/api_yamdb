from rest_framework import serializers
from reviews.models import Category, CHOICES, Genre, Title


class ReviewSerializer(serializers.ModelSerializer):
    pass


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
    pass


class UserEditSerializer(serializers.ModelSerializer):
    pass


class RegisterDataSerializer(serializers.ModelSerializer):
    pass


class TokenSerializer(serializers.Serializer):
    pass


class CommentSerializer(serializers.ModelSerializer):
    pass
