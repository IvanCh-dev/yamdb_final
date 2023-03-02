from api.v1.filters_for_title import CustomTitleFilter
from api.v1.mixins import CreateListDestroy
from api.v1.permissions import IsAdminOrReadOnly, IsModeratorOrAdminOrAuthor
from api.v1.serializers import (CategorySerializer, CommentSerializer,
                                GenreSerializer, ReviewSerializer,
                                TitleGetSerializer, TitlePostSerializer)
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from reviews.models import Category, Genre, Review, Title


class CategoryViewSet(CreateListDestroy):
    """Предсттавление Категории (типы) произведений"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(CreateListDestroy):
    """Представление Категории жанров"""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminOrReadOnly, )
    filter_backends = (DjangoFilterBackend, )
    filterset_class = CustomTitleFilter
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH'):
            return TitlePostSerializer
        return TitleGetSerializer

    def get_queryset(self):
        return Title.objects.annotate(rating=Avg('reviews__score'))


class ReviewViewSet(viewsets.ModelViewSet):
    """Представления Review  для получения и оставления отзыва"""
    serializer_class = ReviewSerializer
    permission_classes = (IsModeratorOrAdminOrAuthor, )
    pagination_class = PageNumberPagination

    def get_queryset(self):
        return get_object_or_404(
            Title, id=self.kwargs.get('title_id')).reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    """Представления Comment комментарии к отзывам"""
    serializer_class = CommentSerializer
    permission_classes = (IsModeratorOrAdminOrAuthor, )
    pagination_class = PageNumberPagination

    def get_queryset(self):
        return get_object_or_404(
            Review, id=self.kwargs.get('review_id'),
            title=self.kwargs.get('title_id')).comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'),
                                   title=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, review=review)
