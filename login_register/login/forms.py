from django import forms
from captcha.fields import CaptchaField
from .models import User


class UserForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=128, 
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(label='密码', max_length=256, 
                                widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    captcha = CaptchaField(label='验证码', error_messages={'invalid': '验证码错误'})


class RegisterForm(forms.Form):
    gender = (
        ('male', '男'),
        ('female', '女'),
    )
    username = forms.CharField(label='用户名', max_length=128, min_length=3,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入3位以上用户名'}))
    password1 = forms.CharField(label='密码', max_length=256,
                                widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '请输入密码'}))
    password2 = forms.CharField(label='确认密码', max_length=256,
                                widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '请再次输入密码'}))
    email = forms.EmailField(label='邮箱', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    # 写法一：
    #sex = forms.ChoiceField(label='性别', choices=gender)
    # 写法二：
    sex = forms.CharField(label='性别', widget=forms.Select(choices=gender))
    captcha = CaptchaField(label='验证码', error_messages={'invalid': '验证码错误'})


class PwdForgetForm(forms.Form):
    email = forms.EmailField(label='邮箱',
                             widget=forms.EmailInput(
                                 attrs={'class': 'form-control', 'placeholder': '请输入绑定过的邮箱'}
                             )
    )
    new_pwd1 = forms.CharField(max_length=256,
                               label='新的密码',
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '请输入新的密码'})
    )

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super(PwdForgetForm, self).__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data['email'].strip()
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError('邮箱不存在')
        return email
