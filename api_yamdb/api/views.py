from rest_framework.views import APIView
from rest_framework import filters, mixins, viewsets
from rest_framework.response import Response
from rest_framework import status, mixins, viewsets, filters
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.decorators import api_view
from django_filters.rest_framework import DjangoFilterBackend
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
import random

from .serializers import (
    GetConfirmationCode,
    CustomGetTokenSerializer,
    GetOrCreateUsersSerializer,
    GetInfoAboutMeSerializer,
    CertainUserSerializer,
    CategorySerializer,
    GenreSerializer,
    TitleSerializer
)
from users.models import User
from reviews.models import Category, Genre, Title


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


class EmailConfirm(APIView):
    """ Регистрируем пользователя совместно с выдачей кода. """

    def post(self, request):
        serializer = GetConfirmationCode(data=request.data)

        if serializer.is_valid():
            # Генерируем код
            confirmation_code = ''
            for i in range(7):
                confirmation_code += str(random.randint(0, 9))

            try:
                user = User.objects.get(
                    username=serializer.validated_data.get('username'))
                user.confirmation_code = confirmation_code
                user.save()
            except User.DoesNotExist:
                serializer.save(confirmation_code=confirmation_code)

            # Отправляем письмо с кодом
            mail = send_mail(
                'Подтверждение почты',
                (
                    f'Ваш код подтверждения: {confirmation_code}\n'
                    f"Никнейм: {serializer.validated_data.get('username')}\n"
                ),
                'send.confirm.code@yandex.ru',
                [serializer.validated_data.get('email')],
            )

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetCustomToken(APIView):

    def post(self, request):
        serializer = CustomGetTokenSerializer(data=request.data)

        if serializer.is_valid():
            try:
                user = User.objects.get(
                    username=serializer.validated_data['username']
                )
                if user.confirmation_code == serializer.validated_data['confirmation_code']:
                    refresh = RefreshToken.for_user(user)

                    return Response(
                        {'token': str(refresh.access_token)},
                        status=status.HTTP_200_OK,
                    )
                return Response('Неверный ключ доступа!', status=status.HTTP_400_BAD_REQUEST)
            except User.DoesNotExist:
                return Response('Пользователя не существует.', status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetOrCreateUsers(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    """ Получаем список пользователей или создаём пользователя """

    queryset = User.objects.all()
    serializer_class = GetOrCreateUsersSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['=username']


@api_view(['GET', 'PATCH'])
def users_me(request):
    """ Методы get и patch к пользователю отправившему запрос. """
    user = get_object_or_404(User, pk=request.user.id)

    if request.method == 'GET':
        serializer = GetInfoAboutMeSerializer(user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    serializer = GetInfoAboutMeSerializer(
        user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CertainUser(viewsets.ViewSet):
    """ Методы get patch и delete к конкретному юзеру. """
    lookup_field = 'username'

    def retrieve(self, request, username=None):
        user = get_object_or_404(User, username=username)
        serializer = CertainUserSerializer(user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def partial_update(self, request, username=None):
        user = get_object_or_404(User, username=username)
        serializer = CertainUserSerializer(
            user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, username=None):
        user = get_object_or_404(User, username=username)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
