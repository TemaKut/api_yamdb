import datetime as dt

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404

from users.models import User
from reviews.models import Category, Genre, Title, Rewiew, Comment


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

class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )
    title = serializers.SlugRelatedField(
        read_only=True, slug_field='id')

    def validate(self, data):
        request = self.context['request']
        author = request.user
        title_id = self.context['view'].kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        score = data['score']

        if request.method == 'POST':
            if Review.objects.filter(title=title, author=author).exists():
                raise ValidationError('Вы можете оставить только'
                                      'один отзыв на произведение')
            if 0 > score > 10:
                raise ValidationError('Оценка')
        return data

    class Meta:
        model = Review
        fields = ('title', 'id', 'text', 'author', 'score', 'pub_date')


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
        read_only_fields = ('id', 'review', 'pub_date')
