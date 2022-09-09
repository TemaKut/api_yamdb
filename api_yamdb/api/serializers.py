import datetime as dt

from rest_framework import serializers

from users.models import User
from reviews.models import Category, Genre, Title


class GetConfirmationCode(serializers.ModelSerializer):
    """ Сериализатор отправки кода на email. """
    confirmation_code = serializers.CharField(required=False, write_only=True)

    class Meta:
        fields = ('email', 'confirmation_code', 'username')
        model = User
        extra_kwargs = {
            'username': {
                'validators': []
            },
            'email': {
                'validators': []
            }
        }


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Category


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )
    genres = serializers.SlugRelatedField(
        slug_field='slug', many=True, queryset=Genre.objects.all()
    )

    class Meta:
        fields = ('name', 'year', 'category', 'genres')
        model = Title

    def validate_year(self, value):
        year = dt.date.today().year
        if value > year:
            raise serializers.ValidationError(
                'Год выпуска произведения не может быть больше нынешнего.'
            )
        return value


class CustomGetTokenSerializer(serializers.Serializer):
    """ Сериализатор получения токена. """

    confirmation_code = serializers.CharField()
    username = serializers.CharField()


class GetOrCreateUsersSerializer(serializers.ModelSerializer):
    """ Создаём или получаем пользователей. """

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )


class GetInfoAboutMeSerializer(serializers.ModelSerializer):
    """ Сериализатор получения информации о пользователе. """

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
        )
        extra_kwargs = {
            'username': {
                'validators': []
            },
            'email': {
                'validators': []
            }
        }


class CertainUserSerializer(serializers.ModelSerializer):
    """ Сериализатор для конкретного пользователя. """

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )
        extra_kwargs = {
            'username': {
                'validators': []
            },
            'email': {
                'validators': []
            }
        }
