from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

from rest_framework import filters, generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from users.models import User
from api.v1.permissions import IsAdmin
from users.serializers import (GettingTokenSerializer, SignupSerializer,
                               UserSerializer)


class SignupUserAPIView(generics.CreateAPIView):
    """Регистрация нового пользователя """
    serializer_class = SignupSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, _ = User.objects.get_or_create(**serializer.validated_data)
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            subject='Confirmation code',
            message=f'Your confirmation code {confirmation_code}',
            from_email='from@example.com',
            recipient_list=[user.email],
            fail_silently=False)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TokenAuthApiView(generics.CreateAPIView):
    """Получение токена """
    serializer_class = GettingTokenSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(
            User, username=serializer.validated_data['username']
        )
        if default_token_generator.check_token(
                user, serializer.validated_data['confirmation_code']):
            return Response(AccessToken.for_user(user))
        return Response(status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    """Обработка запросов к:
    "users/", "users/username/", "users/me/"."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("username",)
    lookup_field = "username"

    @action(
        methods=["get", "patch"],
        detail=False,
        url_path="me",
        permission_classes=(IsAuthenticated,),
    )
    def get_me(self, request):
        if request.method == 'GET':
            serializer = self.get_serializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = self.get_serializer(
            request.user,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(role=request.user.role, partial=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
