from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework import serializers
from reviews.models import Review, Title, Comment


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
