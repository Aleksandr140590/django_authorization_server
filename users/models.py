from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models


# Create your models here.
class UserAccountManager(BaseUserManager):
    """Manager для создания аккаунта пользователя."""

    def create(
        self,
        email,
        name,
        password=None,
        is_active=False,
    ):
        email = email.lower()

        user = self.model(
            email=email,
            name=name,
            is_active=is_active,
        )
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, name, password=None):
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            name=name,
        )

        user.set_password(password)
        user.save()

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)
        return user


class UserModel(AbstractBaseUser, PermissionsMixin):
    """Модель пользователя."""

    email = models.EmailField(
        max_length=50,
        unique=True,
        verbose_name="Электронная почта",
    )
    name = models.CharField(
        max_length=50,
        verbose_name="Имя",
    )
    password = models.CharField(verbose_name="Пароль", max_length=128)
    is_active = models.BooleanField(
        default=False, verbose_name="Пользователь активен"
    )
    is_staff = models.BooleanField(
        verbose_name="Функции администратора", default=False
    )
    person_created = models.DateTimeField(
        "Дата создания аккаунта", auto_now_add=True
    )

    objects = UserAccountManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
