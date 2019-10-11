import hashlib
import time
import datetime
from django.shortcuts import render, redirect
from django.conf import settings

from .tasks import send_email
from .models import User, ConfirmString
from .forms import UserForm, RegisterForm, PwdForgetForm
# Create your views here.


def hash_code(s, salt='login_register'):
    # 哈希加盐加密
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())    # update方法只接收bytes类型
    return h.hexdigest()    # 获得16进制str类型的消息摘要


def make_confirm_string(user):
    """
    确认码验证
    :param user:
    :return:
    """
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    code = hash_code(user.name, now)
    ConfirmString.objects.create(code=code, user=user,)
    return code


def index(request):
    """
    首页
    :param request:
    :return:
    """
    return render(request, 'login/index.html')


def login(request):
    """
    登录界面
    :param request:
    :return:
    """
    # 通过session会话判断是否已登录
    if request.session.get('is_login', ''):
        # 已登录的话，则直接返回首页
        return redirect('/index/')
    if request.method == 'POST':
        login_form = UserForm(request.POST)
        message = '请检查填写的内容'
        if login_form.is_valid():
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            try:
                user = User.objects.get(name=username)
                if not user.has_confirmed:
                    message = '该用户尚未通过邮件确认'
                    return render(request, 'login/login.html', locals())
                if user.password == hash_code(password):    # 哈希值与数据库的值相比较
                    # 往session字典内写入用户状态和数据，当然完全可以往里面写任何数据，不仅仅限于用户相关！
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.name
                    return redirect('/index/')
                else:
                    message = '密码不正确'
            except:
                message = '用户名不存在'
        return render(request, 'login/login.html', locals())
    login_form = UserForm()
    return render(request, 'login/login.html', locals())


def register(request):
    """
    注册界面
    :param request:
    :return:
    """
    if request.session.get('is_login', ''):
        # 登录状态不允许注册
        return redirect('/index/')
    if request.method == 'POST':
        register_form = RegisterForm(request.POST)
        message = '请检查填写的内容'
        if register_form.is_valid():
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            email = register_form.cleaned_data['email']
            sex = register_form.cleaned_data['sex']
            if password1 != password2:
                message = '两次输入的密码不一致，请重新输入！'
                return render(request, 'login/register.html', locals())
            else:
                # 用户名检查
                same_name_user = User.objects.filter(name=username)
                if same_name_user:  # 用户名唯一
                    message = '用户名已经存在， 请重新选择用户名'
                    return render(request, 'login/register.html', locals())
                # 邮箱检查
                same_email_user = User.objects.filter(email=email)
                if same_email_user:
                    message = '该邮箱地址已经被注册，请使用别的邮箱'
                    return render(request, 'login/register.html', locals())

                # 检查完毕，一切ok啦，创建新的用户
                new_user = User()
                new_user.name = username
                new_user.password = hash_code(password2)
                new_user.email =email
                new_user.sex = sex
                new_user.save()

                code = make_confirm_string(new_user)
                # celery异步发送邮件
                print("开始发送邮件，请注意查收")
                send_email.delay(email, code)

                return redirect('/login/') # 注册完,自动跳转到登录页面
    else:
        register_form = RegisterForm()
    return render(request, 'login/register.html', {'register_form': register_form})


def logout(request):
    """
    登出功能
    :param request:
    :return:
    """
    if not request.session.get('is_login', ''):
        return redirect('/index/')
    request.session.flush()
    return redirect('/index/')


def user_confirm(request):
    """
    用户确认功能
    :param request:
    :return:
    """
    code = request.GET.get('code', '')
    message = ''
    try:
        confirm = ConfirmString.objects.get(code=code)
    except:
        message = '无效的确认请求！'
        return render(request, 'login/confirm.html', locals())

    c_time = confirm.c_time
    now = datetime.datetime.now()
    if now > c_time + datetime.timedelta(settings.CONFIRM_DAYS):
        confirm.user.delete()
        message = '您的邮件已过期，请重新注册！'
        return render(request, 'login/confirm.html', locals())
    else:
        confirm.user.has_confirmed = True
        confirm.user.save()
        # confirm.delete()
        message = '感谢确认，请使用账户登录'
        return render(request, 'login/confirm.html', locals())


def pwd_forget(request):
    """
    密码忘记找回功能
    :param request:
    :return:
    """
    if request.session.get('is_login', ''):
        return redirect('/index/')
    if request.method == 'POST':
        pwdforget_form = PwdForgetForm(request.POST, request=request)
        message = '请检查填写的内容'
        if pwdforget_form.is_valid():
            email = pwdforget_form.cleaned_data['email']
            new_pwd1 = pwdforget_form.cleaned_data['new_pwd1']
            try:
                user = User.objects.get(email=email)
                user.password = hash_code(new_pwd1)
                user.save()
                return redirect('/login/')
            except:
                message = "输入的邮箱不存在"
        return render(request, 'login/pwd_forget.html', locals())
    pwdforget_form = PwdForgetForm()
    return render(request, 'login/pwd_forget.html', locals())
