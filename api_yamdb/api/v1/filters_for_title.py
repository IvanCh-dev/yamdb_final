from django_filters.rest_framework import CharFilter, FilterSet, NumberFilter

from reviews.models import Title


class CustomTitleFilter(FilterSet):
    """
    фильтрует по полю slug категории,
    фильтрует по полю slug жанра,
    фильтрует по названию произведения,
    фильтрует по году
    """
    genre = CharFilter(field_name='genre__slug',)
    category = CharFilter(field_name='category__slug',)
    year = NumberFilter(field_name='year',)
    name = CharFilter(field_name='name', lookup_expr='contains')

    class Meta:
        model = Title
        fields = ('genre', 'category', 'year', 'name')
