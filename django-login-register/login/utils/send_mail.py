#!usr/bin/env python
# -*- coding:utf-8 -*-
import os
from django.core.mail import EmailMultiAlternatives
from django.conf import settings


def send_email(email, code):
    subject = '来自测试邮件'
    text_content = '欢迎访问,如果你看到这条消息，说明你的邮箱服务器不提供HTML链接功能，请联系管理员！'
    html_content = '''<p>感谢注册<a href="http://{0}/confirm/?code={1}" target=blank>www.xxxxxx.com</a>，\
                    这是由python+Django开发的注册登录系统！</p>
                    <p>请点击站点链接完成注册确认！</p>
                    <p>此链接有效期为{2}天！</p>
                    '''.format('127.0.0.1:9000', code, settings.CONFIRM_DAYS)
    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [email])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()
