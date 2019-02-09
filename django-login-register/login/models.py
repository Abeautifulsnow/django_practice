from django.db import models

# Create your models here.


class User(models.Model):
    name = models.CharField(max_length=128, verbose_name='用户名')
    password = models.CharField(max_length=256, verbose_name='密码')
    email = models.EmailField(unique=True, verbose_name='邮箱')
    sex = models.CharField(max_length=32, choices=(('male', '男'), ('female', '女')), default='男', verbose_name='性别')
    c_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    has_confirmed = models.BooleanField(default=False, verbose_name='是否确认')

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name
        ordering = ['-c_time']

    def __str__(self):
        return self.name


class ConfirmString(models.Model):
    code = models.CharField(max_length=256, verbose_name='验证码')
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='用户')
    c_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '确认码'
        verbose_name_plural = verbose_name
        ordering = ['-c_time']

    def __str__(self):
        return self.user.name + ": " + self.code
