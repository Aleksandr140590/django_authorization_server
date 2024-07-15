from django.utils.deprecation import MiddlewareMixin
from django.http.request import HttpRequest
from django.http.response import HttpResponseBase
from http import cookies

from config.settings import SIMPLE_JWT


cookies.Morsel._flags.add("partitioned")
cookies.Morsel._reserved.setdefault("partitioned", "Partitioned")


BACK_COOKIES = [
    SIMPLE_JWT["AUTH_ACCESS_COOKIE"],
    SIMPLE_JWT["AUTH_REFRESH_COOKIE"],
]


class CookiePartitioningMiddleware(MiddlewareMixin):
    """Добавляет к Кукам атрибут Partitioned"""

    def process_response(
        self, request: HttpRequest, response: HttpResponseBase
    ) -> HttpResponseBase:
        if (
            not request.user.is_authenticated
            and request.COOKIES.get(SIMPLE_JWT["AUTH_ACCESS_COOKIE"])
            and request.path != "/auth/jwt/create/"
        ):
            response.delete_cookie(SIMPLE_JWT["AUTH_ACCESS_COOKIE"])
            return response

        for name in BACK_COOKIES:
            if cookie := response.cookies.get(name):
                cookie["Partitioned"] = True

        return response
