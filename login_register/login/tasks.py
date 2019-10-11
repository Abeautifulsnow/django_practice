from django.core.mail import EmailMultiAlternatives
from django.conf import settings

from login_register import celery_app


@celery_app.task
def send_email(email, code):
    print("发送邮件中...")
    subject = '来自测试邮件'
    text_content = '欢迎访问,如果你看到这条消息，说明你的邮箱服务器不提供HTML链接功能，请联系管理员！'
    html_content = '''<p>感谢注册<a href="http://{0}/confirm/?code={1}" target=blank>www.xxxxxx.com</a>，\
                    这是由python+Django开发的注册登录系统！</p>
                    <p>请点击站点链接完成注册确认！</p>
                    <p>此链接有效期为{2}天！</p>
                    '''.format('127.0.0.1:8000', code, settings.CONFIRM_DAYS)
    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [email])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()
    print("已发送成功...")
