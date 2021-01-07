# Generated by Django 2.2.5 on 2019-09-23 11:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Goods',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goods_name', models.CharField(max_length=100, verbose_name='商品名称')),
                ('goods_price', models.FloatField(default=0.0, verbose_name='商品价格')),
            ],
            options={
                'verbose_name': '商品',
                'verbose_name_plural': '商品',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_num', models.CharField(max_length=64, verbose_name='订单序号')),
                ('order_status', models.IntegerField(choices=[(0, '未支付'), (1, '已支付')], default=0)),
                ('goods', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='demo.Goods', verbose_name='商品名字')),
            ],
            options={
                'verbose_name': '订单信息',
                'verbose_name_plural': '订单信息',
            },
        ),
    ]
