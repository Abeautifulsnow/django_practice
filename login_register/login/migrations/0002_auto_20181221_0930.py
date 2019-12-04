# Generated by Django 2.1.4 on 2018-12-21 09:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConfirmString',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=256, verbose_name='验证码')),
                ('c_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
            ],
            options={
                'verbose_name': '确认码',
                'verbose_name_plural': '确认码',
                'ordering': ['-c_time'],
            },
        ),
        migrations.AddField(
            model_name='user',
            name='has_confirmed',
            field=models.BooleanField(default=False, verbose_name='是否确认'),
        ),
        migrations.AlterField(
            model_name='user',
            name='c_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name='创建时间'),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, unique=True, verbose_name='邮箱'),
        ),
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.CharField(max_length=128, verbose_name='用户名'),
        ),
        migrations.AlterField(
            model_name='user',
            name='sex',
            field=models.CharField(choices=[('male', '男'), ('female', '女')], default='男', max_length=32, verbose_name='性别'),
        ),
        migrations.AddField(
            model_name='confirmstring',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='login.User', verbose_name='用户'),
        ),
    ]