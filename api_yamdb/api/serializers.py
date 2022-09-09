from rest_framework import serializers

from users.models import User


class GetConfirmationCode(serializers.ModelSerializer):
    """ Сериализатор отправки кода на email. """
    confirmation_code = serializers.CharField(required=False, write_only=True)

    class Meta:
        fields = ('email', 'confirmation_code', 'username')
        model = User
        extra_kwargs = {
            'username': {
                'validators': []
            },
            'email': {
                'validators': []
            }
        }


class CustomGetTokenSerializer(serializers.Serializer):
    """ Сериализатор получения токена. """

    confirmation_code = serializers.CharField()
    username = serializers.CharField()


class GetOrCreateUsersSerializer(serializers.ModelSerializer):
    """ Создаём или получаем пользователей. """

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )


class GetInfoAboutMeSerializer(serializers.ModelSerializer):
    """ Сериализатор получения информации о пользователе. """

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
        )
        extra_kwargs = {
            'username': {
                'validators': []
            },
            'email': {
                'validators': []
            }
        }


class CertainUserSerializer(serializers.ModelSerializer):
    """ Сериализатор для конкретного пользователя. """

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )
        extra_kwargs = {
            'username': {
                'validators': []
            },
            'email': {
                'validators': []
            }
        }
