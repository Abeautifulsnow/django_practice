import jwt
import datetime
from django.db import models
from django.contrib.auth.models import PermissionsMixin, UserManager, AbstractBaseUser
from django_jwt.settings import SECRET_KEY


# Create your models here.


class User(AbstractBaseUser, PermissionsMixin):
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    username = models.EmailField(max_length=255, unique=True, verbose_name='用户名')
    email = models.EmailField(max_length=255, unique=True, verbose_name='邮箱')
    fullname = models.CharField(max_length=64, null=True, verbose_name='中文名')
    phonenumber = models.CharField(max_length=16, null=True, unique=True, verbose_name='电话')
    is_active = models.BooleanField(default=True, verbose_name='激活状态')

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username

    @property
    def token(self):
        return self._generate_jwt_token()
    
    def _generate_jwt_token(self):
        token = jwt.encode({
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
            'iat': datetime.datetime.utcnow(),
            'data': {
                'username': self.username,
            }
        }, SECRET_KEY, algorithm='HS256')
        
        return token.decode("utf-8")
    
    class Meta:
        default_permissions = ()
    
        permissions = (
            ("select_user", "查看用户"),
            ("change_user", "修改用户"),
            ("delete_user", "删除用户"),
        )
