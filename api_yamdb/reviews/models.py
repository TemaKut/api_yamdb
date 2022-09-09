from django.db import models


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
