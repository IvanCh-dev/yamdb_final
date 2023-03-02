from django.core.exceptions import ValidationError
from rest_framework import serializers
from users.models import User


class ValidationUser:
    """Validation username."""

    def validate_username(self, value):
        if value == '':
            raise ValidationError('поле username не заполненно')
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('username занято')
        if value == 'me':
            raise ValidationError('me недопустимо в username')
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                'email занят'
            )
        return value


class SignupSerializer(serializers.Serializer, ValidationUser):
    '''Сериализация auth/signup.'''
    username = serializers.CharField(required=True, max_length=150)
    email = serializers.EmailField(required=True, max_length=150)


class GettingTokenSerializer(serializers.Serializer, ValidationUser):
    '''Сериализация get_token.'''
    username = serializers.CharField(required=True, max_length=150)
    confirmation_code = serializers.CharField(required=True)


class UserSerializer(serializers.ModelSerializer):
    '''Сериализация данных User.'''

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
