from typing import List, Optional

from drf_yasg import openapi

from config.settings import SWAGGER_TAGS

DEFAULT_TAG = SWAGGER_TAGS.get("users")

RESPONSE_400 = lambda msg: openapi.Response(description="BadRequest: " + msg)
RESPONSE_401 = lambda msg: openapi.Response(description="Unauthorized: " + msg)
RESPONSE_403 = lambda msg: openapi.Response(description="Forbidden: " + msg)


class BaseSwaggerSchema:
    operation_description: str
    request_body: Optional[openapi.Schema]
    manual_parameters: Optional[List[openapi.Parameter]]
    responses: openapi.Responses


class TokenJWTCreateDocs(BaseSwaggerSchema):
    tags = [SWAGGER_TAGS.get("auth")]
    operation_id = "jwt-create"
    operation_summary = "Получение токена авторизации"
    operation_description = (
        "Используйте этот метод для получения JWT токена авторизации."
    )
    responses = {
        200: openapi.Response(
            "При верно введенных данных возвращается refresh и "
            "access токены",
            openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "refresh": openapi.Schema(
                        type=openapi.TYPE_STRING, title="токен обновления"
                    ),
                    "access": openapi.Schema(
                        type=openapi.TYPE_STRING, title="JWT токен авторизации"
                    ),
                },
            ),
        ),
    }


class TokenJWTVerify(BaseSwaggerSchema):
    tags = [SWAGGER_TAGS.get("auth")]
    method = "get"


class TokenJWTRefresh(BaseSwaggerSchema):
    tags = [SWAGGER_TAGS.get("auth")]
    method = "post"


class TokenJWTCreate(BaseSwaggerSchema):
    tags = [SWAGGER_TAGS.get("auth")]
    method = "post"
