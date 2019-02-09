from django.contrib import admin
from login.models import User, ConfirmString
# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'password', 'email', 'sex', 'has_confirmed', 'c_time')


@admin.register(ConfirmString)
class ConfirmStringAdmin(admin.ModelAdmin):
    list_display = ('user', 'code', 'c_time', )
