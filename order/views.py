from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from cart.models import ShoppingCart
from fresh_shop.settings import ORDER_NUMBER
from order.models import OrderInfo, OrderGoods
from user.models import UserAddress
from utlis.function import get_order_sn


def place_order(request):
    if request.method == 'GET':
        # 获取当前登录系统的用户
        user = request.user
        carts = ShoppingCart.objects.filter(user=user, is_select=True).all()
        # 计算小计和总价
        total_price = 0
        for cart in carts:
            # 小计金额
            price = cart.goods.shop_price * cart.nums
            cart.goods_price = price
            # 总金额
            total_price += price
        num = 0
        session_goods = request.session.get('goods')
        for se_goods in session_goods:
            if se_goods[2]:
                num += 1
        # 获取当前登录系统的用户的收获地址信息
        address = UserAddress.objects.filter(user_id=user.id).all()
        return render(request, 'place_order.html',
                      {'carts': carts, 'total_price': total_price, 'num': num, 'address': address})


def order(request):
    if request.method == 'POST':
        # 1.获取收获地址id值
        ad_id = request.POST.get('ad_id')
        # 2.创建订单
        order_sn = get_order_sn()
        user_id = request.session.get('user_id')

        # 计算订单金额
        shop_cart = ShoppingCart.objects.filter(user_id=user_id,
                                                is_select=True)
        order_mount = 0
        for cart in shop_cart:
            order_mount += cart.goods.shop_price * cart.nums

        # 收获信息
        user_address = UserAddress.objects.filter(pk=ad_id).first()
        order = OrderInfo.objects.create(user_id=user_id,
                                         order_sn=order_sn,
                                         order_mount=order_mount,
                                         address=user_address.address,
                                         signer_name=user_address.signer_name,
                                         signer_mobile=user_address.signer_mobile)
        # 3.创建订单详情
        for cart in shop_cart:
            OrderGoods.objects.create(order=order,
                                      goods=cart.goods,
                                      goods_nums=cart.nums)

        # 4.删除购物车
        shop_cart.delete()
        session_goods = request.session.get('goods')
        for se_goods in session_goods[:]:
            if se_goods[2]:
                session_goods.remove(se_goods)
        request.session['goods'] = session_goods

        return JsonResponse({'code': 200, 'msg': '请求成功'})

def user_order(request):
    if request.method == 'GET':
        page = int(request.GET.get('page', 1))
        #获取登陆系统用户的id
        user_id = request.session.get('user_id')
        #查询当前用户产生的订单信息
        orders = OrderInfo.objects.filter(user_id=user_id)
        status = OrderInfo.ORDER_STATUS
        #分页
        pg = Paginator(orders, ORDER_NUMBER)
        orders = pg.page(page)
        activate = 'order'
        return render(request, 'user_center_order.html',
                      {'orders': orders,
                       'status': status,
                       'activate':activate})
