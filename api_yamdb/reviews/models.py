from datetime import datetime

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from users.models import User


class Category(models.Model):
    """Модель для работы с категориями произведений"""
    name = models.CharField(max_length=256,
                            verbose_name='Категория'
                            )
    slug = models.SlugField(unique=True,
                            verbose_name='Адрес')

    class Meta:
        verbose_name = "Катеогория произведения"
        verbose_name_plural = "Катеогории произведений"

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Модель для работы с жанрами произведений"""
    name = models.CharField(max_length=256,
                            verbose_name='Жанр'
                            )
    slug = models.SlugField(unique=True,
                            verbose_name='Адрес')

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

    def __str__(self):
        return self.name


class Title(models.Model):
    """Модель для работы с произведениями"""
    name = models.CharField(max_length=255,
                            verbose_name='Название произведения')
    """Одно произведение может быть привязано к нескольким жанрам."""
    genre = models.ManyToManyField(Genre,
                                   through='TitleGenre',
                                   through_fields=('title', 'genre'),
                                   verbose_name='Жанр произведения'
                                   )
    description = models.TextField(max_length=255,
                                   verbose_name='Описание произведения',
                                   null=True,
                                   blank=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='category',
        verbose_name='Название Категории'
    )
    year = models.PositiveIntegerField(
        validators=(MaxValueValidator(
                    datetime.now().year,
                    message=(
                        'Нельзя добавлять произведения,которые еще не вышли'),
                    ),
                    ),
        verbose_name='Дата публикации',
    )

    class Meta:
        ordering = ('name',)
        verbose_name = "Произведение"
        verbose_name_plural = "Произведения"

    def __str__(self):
        return self.name


class TitleGenre(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='genretitles',
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.SET_NULL,
        null=True,
        related_name='genretitles',
    )

    class Meta:
        verbose_name = "Жанр произведения"
        verbose_name_plural = "Жанры произведения"

    def __str__(self):
        return f'{self.title} произведение имеет жанр: {self.genre}'


class Review(models.Model):
    text = models.TextField(verbose_name='Текст отзыва')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews',
        verbose_name='Автор отзыва')
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews',
        verbose_name='Название произведения')
    score = models.IntegerField(validators=[
        MaxValueValidator(10),
        MinValueValidator(1)
    ], verbose_name='Оценка')
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)

    class Meta:
        """Создана уникальность полей
        произведения и человека который оставил отзыв на него"""
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_author_title'
            )
        ]
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


class Comment(models.Model):
    text = models.TextField(verbose_name='Текст комментария')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments',
        verbose_name='Автор комментария')
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments',
        verbose_name='Отзыв')
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text
