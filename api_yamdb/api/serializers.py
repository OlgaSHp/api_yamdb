from rest_framework import serializers



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
    pass


class UserEditSerializer(serializers.ModelSerializer):
    pass


class RegisterDataSerializer(serializers.ModelSerializer):
    pass


class TokenSerializer(serializers.Serializer):
    pass


class CommentSerializer(serializers.ModelSerializer):
    pass
