from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt import views

from .swagger_documentation.users import (
    TokenJWTVerify,
    TokenJWTRefresh,
    TokenJWTCreate,
)
from .views import (
    CustomUserViewSet,
    CustomTokenObtainPairView,
    auth_jwt_verify,
    CustomRefreshTokenView,
    CustomTokenRefreshView,
)

from drf_yasg.utils import swagger_auto_schema


user_router = routers.DefaultRouter()
user_router.register(r"users", CustomUserViewSet, basename="custom_users")


def is_route_selected(url_pattern):
    urls = [
        "users/reset_email/",
        "users/reset_email_confirm/",
        "users/activation/",
        "users/resend_activation/",
        "users/reset_password/",
        "users/reset_password_confirm/",
        "users/set_email/",
        "users/set_password/",
    ]

    for u in urls:
        match = url_pattern.resolve(u)
        if match:
            return False
    return True


selected_user_routes = list(filter(is_route_selected, user_router.urls))

# Декораторы документации SWAGGER
decorated_jwt_create_view = swagger_auto_schema(**TokenJWTCreate.__dict__)(
    CustomTokenObtainPairView.as_view()
)

decorated_jwt_verify_view = swagger_auto_schema(**TokenJWTVerify.__dict__)(
    auth_jwt_verify
)

decorated_jwt_refresh_view = swagger_auto_schema(**TokenJWTRefresh.__dict__)(
    CustomTokenRefreshView.as_view()
)

urlpatterns = [
    path(
        "",
        include(selected_user_routes),
        name="authentication",
    ),
    path(
        "auth/jwt/create/",
        decorated_jwt_create_view,
        name="jwt-create",
    ),
    path(
        "auth/jwt/refresh/",
        decorated_jwt_refresh_view,
        name="jwt-refresh",
    ),
    path(
        "auth/authverify/", decorated_jwt_verify_view, name="auth-jwt-verify"
    ),
]
