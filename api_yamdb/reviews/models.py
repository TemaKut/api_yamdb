from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class User():
    pass


class Title():
    pass


class Category():
    pass


class Genre():
    pass


class Review(models.Model):
    review_id = models.AutoField(primary_key=True)
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
        validators=(MinValueValidator(1, 'Допустимые значения от 1 до 10'), MaxValueValidator(10))
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
    comment_id = models.AutoField(primary_key=True)
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