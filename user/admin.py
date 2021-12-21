from django.contrib import admin
from user.models import User
from django.contrib.auth.admin import UserAdmin

# # Register your models here.
# class UserAdmin(UserAdmin):
#     model = User
#     ordering = ("email",)
#     exclude = ("date_joined",)
#     list_display = ("email",)
#     list_filter = ()


admin.site.register(User)
