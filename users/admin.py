from django.contrib import admin

from users.models import UserModel


@admin.register(UserModel)
class UserModelAdmin(admin.ModelAdmin):
    list_display = ["email", "name", "is_active", "id"]
    list_display_links = ("email",)
