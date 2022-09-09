from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets

from reviews.models import Category, Genre, Title
from .serializers import CategorySerializer, GenreSerializer, TitleSerializer


class CreateListDestroyViewSet(
    mixins.CreateModelMixin, mixins.ListModelMixin,
    mixins.DestroyModelMixin, viewsets.GenericViewSet
):
    """Миксин для создания, удаления и получение списка обьектов"""
    pass


class TitleViewSet(viewsets.ModelViewSet):
    """Класс представления произведений"""
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('name', 'year', 'category__slug', 'genres__slug',)


class CategoryViewSet(CreateListDestroyViewSet):
    """Класс представления категорий произведений"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(CreateListDestroyViewSet):
    """Класс представления жанров произведений"""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
