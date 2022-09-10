from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator



class Category(models.Model):
    """Модель категорий произведений."""
    name = models.CharField(max_length=50, verbose_name='Название')
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']


class Genre(models.Model):
    """Модель жанров произведений."""
    name = models.CharField(max_length=50, verbose_name='Название')
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ['name']


class Title(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название')
    year = models.IntegerField()
    description = models.TextField(blank=True, null=True)
    rating = models.IntegerField(
        null=True, default=None, verbose_name='Рейтинг'
    )
    category = models.ForeignKey(
        Category, related_name='titles', on_delete=models.SET_NULL, null=True
    )
    genres = models.ManyToManyField(Genre, through='GenreTitle')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ['name']


class GenreTitle(models.Model):
    genre = models.ForeignKey(
        Genre, on_delete=models.CASCADE, verbose_name='Произведение'
    )
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, verbose_name='Жанр'
    )

    def __str__(self):
        return f'{self.genre} {self.title}'

    class Meta:
        verbose_name = 'Произведение и жанр'
        verbose_name_plural = 'Произведения и жанры'


class Review(models.Model):
    """Класс для представления отзывов и оценок на произведения titles."""
    title = models.ForeignKey(
        Title,
        verbose_name='Произведение',
        related_name='reviews',
        on_delete=models.CASCADE
    )
    text = models.TextField(verbose_name='Текст')
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        related_name='reviews',
        on_delete=models.CASCADE
    )
    score = models.PositiveSmallIntegerField(
        verbose_name='Оценка пользователей',
        validators=[
            MinValueValidator(1, 'Диапазон значений от 1 до 10'),
            MaxValueValidator(10, 'Диапазон значений от 1 до 10')
        ]
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True
    )

    class Meta:
        ordering = ['pub_date']
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_review'
            ),
        ]

    def __str__(self):
        return self.text


class Comment(models.Model):
    """Класс для представления комментариев к отзывам."""
    review = models.ForeignKey(
        Review,
        verbose_name='Отзыв',
        related_name='comments',
        on_delete=models.CASCADE,
    )
    text = models.TextField(verbose_name='Текст')
    author = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        related_name='comments',
        on_delete=models.CASCADE
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['pub_date']

    def __str__(self):
        return self.text
