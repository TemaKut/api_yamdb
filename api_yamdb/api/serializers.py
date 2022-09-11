import datetime as dt
from django.db.models import Avg

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404

from users.models import User
from reviews.models import Category, Genre, Title, Review, Comment


class GetConfirmationCode(serializers.ModelSerializer):
    """ Сериализатор отправки кода на email. """
    confirmation_code = serializers.CharField(required=False, write_only=True)

    def validate(self, data):
        username = data['username']
        if username == 'me':
            raise ValidationError('Запрещённое имя пользователя.')
        return data

    class Meta:
        fields = ('email', 'confirmation_code', 'username')
        model = User


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug', many=True, queryset=Genre.objects.all()
    )

    class Meta:
        fields = ('id', 'name', 'year', 'description', 'category', 'genre')
        model = Title

    def validate_year(self, value):
        year = dt.date.today().year
        if value > year:
            raise serializers.ValidationError(
                'Год выпуска произведения не может быть больше нынешнего.'
            )
        return value


class TitleReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    genre = GenreSerializer(many=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        fields = '__all__'
        model = Title

    def get_rating(self, obj):
        rating = obj.reviews.aggregate(Avg(('score')))
        return rating.get('score__avg')


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

    def validate(self, data):

        if (
            self.context.get('request').user.role == 'user'
            and data.get('role')
        ):
            raise ValidationError('Вам нельзя менять свою роль.')

        return data

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
        extra_kwargs = {'role': {'read_only': True}}


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
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('id', 'review', 'pub_date')
