from rest_framework import filters, mixins, viewsets
from rest_framework.pagination import PageNumberPagination

from api.v1.permissions import IsAdminOrReadOnly


class CreateListDestroy(mixins.ListModelMixin,
                        mixins.CreateModelMixin,
                        mixins.DestroyModelMixin,
                        viewsets.GenericViewSet):
    permission_classes = (IsAdminOrReadOnly, )
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=name',)
    lookup_field = 'slug'
