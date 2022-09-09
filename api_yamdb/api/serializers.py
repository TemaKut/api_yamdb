import datetime as dt

from rest_framework import serializers

from reviews.models import Category, Genre, Title


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
