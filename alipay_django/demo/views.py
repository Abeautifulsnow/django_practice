import uuid
from urllib.parse import parse_qs
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from demo.models import Goods, Order
from utils.pay_api import AliPay
from alipay_django225.settings import private_key_path, ali_pub_key_path

# Create your views here.


def goods(request):
    goods_list = Goods.objects.all()
    context = {
        'goods_list': goods_list,
    }
    
    return render(request, 'demo/goods.html', context)


def purchase(request, goods_id):
    """
    订单支付
    :param request:
    :param goods_id:
    :return:跳转到支付宝订单页面
    """
    # 获取商品信息，因为向支付宝接口发送请求的时候需要携带该商品相关信息
    obj_goods = Goods.objects.filter(pk=goods_id)[0]
    '''
    生成订单
    '''
    order_number = str(uuid.uuid4())
    Order.objects.create(
        order_num=order_number,
        goods=obj_goods,
    )
    '''
    跳转到支付宝页面
    '''
    alipay = AliPay(
        appid='2016092500591336',
        app_notify_url=' ',
        return_url=' ',
        app_private_key_path=private_key_path,      # 应用私钥
        alipay_public_key_path=ali_pub_key_path,    # 支付宝公钥
        debug=True
    )

    query_params = alipay.direct_pay(
        subject=obj_goods.goods_name,
        out_trade_no=order_number,
        total_amount=obj_goods.goods_price,
    )

    pay_url = 'https://openapi.alipaydev.com/gateway.do?{0}'.format(query_params)
    return redirect(pay_url)


def show_msg(request):
    if request.method == "GET":
        alipay = AliPay(
            appid='2016092500591336',
            app_notify_url='127.0.0.1:8000/check_order/',
            return_url='127.0.0.1:8000/show_msg/',
            app_private_key_path=private_key_path,  # 应用私钥
            alipay_public_key_path=ali_pub_key_path,  # 支付宝公钥
            debug=True
        )
        params = request.GET.dict()     # 获取请求携带的参数并转换成字典类型
        print(request.GET)
        print(params)
        sign = params.pop('sign', None)     # 获取sign值
        # 对sign进行验证
        status = alipay.verify(params, sign)
        if status:
            return render(request, 'demo/show_msg.html', {'msg': '支付成功'})
        else:
            return render(request, 'demo/show_msg.html', {'msg': '支付失败'})
    else:
        return render(request, 'demo/show_msg.html', {'msg': '只支持GET请求，不支持其他请求。'})


@csrf_exempt
def check_order(request):
    """
    支付宝通知支付的结果信息，如果支付成功可以用来修改订单的状态
    :param request:
    :return:
    """
    if request.method == "POST":
        alipay = AliPay(
            appid='2016092500591336',
            app_notify_url='http://106.12.115.136:8000//check_order/',
            return_url='127.0.0.1:8000/show_msg/',
            app_private_key_path=private_key_path,  # 应用私钥
            alipay_public_key_path=ali_pub_key_path,  # 支付宝公钥
            debug=True
        )
        body_str = request.body.decode("utf-8")
        post_data = parse_qs(body_str)  # 根据&符号分割
        print(post_data)
        post_dict = {}
        for k, v in post_data.items():
            post_dict[k] = v[0]
        sign = post_dict.pop('sign', '')
        status = alipay.verify(post_dict, sign)
        if status:
            out_trade_no = post_data['out_trade_no']
            Order.objects.filter(order_num=out_trade_no).update(order_status=1)
            return HttpResponse("success")
        else:
            return HttpResponse("支付失败")
    else:
        return HttpResponse("只支持POST请求")


def order_list(request):
    order_obj = Order.objects.all()
    context = {
        'order_obj': order_obj,
    }
    
    return render(request, "demo/order_list.html", context)
