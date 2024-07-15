import jwt
from django.contrib.auth import get_user_model
from djoser.views import UserViewSet
from rest_framework import status

from rest_framework.decorators import api_view, permission_classes

from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.views import TokenViewBase
from rest_framework_simplejwt.settings import api_settings

from config import settings
from config.settings import SECRET_KEY, SIMPLE_JWT

User = get_user_model()


def add_tokens_to_response(access_token, refresh_token, response):

    response.set_cookie(
        key=settings.SIMPLE_JWT["AUTH_ACCESS_COOKIE"],
        value=access_token,
        expires=settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"],
        secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
        httponly=settings.SIMPLE_JWT["AUTH_COOKIE_HTTP_ONLY"],
        samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
    )
    if refresh_token:
        response.set_cookie(
            key=settings.SIMPLE_JWT["AUTH_REFRESH_COOKIE"],
            value=refresh_token,
            expires=settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"],
            secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
            httponly=settings.SIMPLE_JWT["AUTH_COOKIE_HTTP_ONLY"],
            samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
        )
    return response


class CustomUserViewSet(UserViewSet):
    pass


class CustomTokenViewBase(TokenViewBase):
    def post(self, request, *args, **kwargs):
        """
        Создание JWT токенов (access & refresh) и добавление токенов в Куки.
        """
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        response = Response(
            serializer.validated_data, status=status.HTTP_201_CREATED
        )

        return add_tokens_to_response(
            serializer.validated_data["access"],
            serializer.validated_data["refresh"],
            response,
        )


class CustomRefreshTokenView(TokenViewBase):

    def post(self, request, *args, **kwargs):
        """
        Обновление JWT токена и добавление токенов в Куки.
        Refresh токен передается в data или используется из Куков
        """
        if not request.data.get("refresh"):
            request.data["refresh"] = request.COOKIES.get(
                "refresh_token", None
            )

        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            response = Response(
                "Authorization error", status=status.HTTP_401_UNAUTHORIZED
            )
            response.delete_cookie(settings.SIMPLE_JWT["AUTH_REFRESH_COOKIE"])
            return response

        response = Response(
            serializer.validated_data, status=status.HTTP_201_CREATED
        )
        return add_tokens_to_response(
            serializer.validated_data["access"], None, response
        )


class CustomTokenObtainPairView(CustomTokenViewBase):
    _serializer_class = api_settings.TOKEN_OBTAIN_SERIALIZER


@api_view(["GET"])
@permission_classes([AllowAny])
def auth_jwt_verify(request):
    """
    Проверка валидности токена в Куках. Возвращает ответ 200 при действительном токене и 401 при ошибке.
    Положительный ответ добавляет Токен в headers для расшифровки и использовании в других сервисах.
    """
    jwt_token = request.COOKIES.get(SIMPLE_JWT["AUTH_ACCESS_COOKIE"])
    if not jwt_token:
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    try:
        payload = jwt.decode(jwt_token, SECRET_KEY, algorithms=["HS256"])
        user = User.objects.get(id=payload["user_id"])
    except Exception:
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    response = Response(status=status.HTTP_200_OK)
    response.headers["X-Token"] = str(jwt_token)
    return response


class CustomTokenRefreshView(CustomRefreshTokenView):
    _serializer_class = api_settings.TOKEN_REFRESH_SERIALIZER
