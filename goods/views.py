from django.http import response
from django.shortcuts import render

# Create your views here.
from goods.models import Goods, GoodsCategory
from user.models import User


def index(request):
    if request.method == 'GET':
        #如果访问首页,返回渲染的首页index.html页面
        #思路:组装结果[object1,object2,object3,object4,object5,object6]
        #组装结果的对象object:包括分类,该分类的前面四个商品信息
        #方式1: object==>[GoodsCategory Object,[Goods object1,Goods object1,Goods object1,Goods object1,]]
        #方式2: object==>{'category_name':[Goods object1,Goods object2,Goods object3,Goods object4]}
        categorys = GoodsCategory.objects.all()
        result = []
        for category in categorys:
            goods = category.goods_set.all()[:4]
            data = [category, goods]
            result.append(data)
            category_type = GoodsCategory.CATEGORY_TYPE
        return render(request, 'index.html', {'result': result, 'category_type':category_type})

def cart(request):
    if request.method == 'GET':
        return render(request, 'cart.html')

def detail(request, id):
    if request.method == 'GET':
        # 返回详情页面解析
        goods = Goods.objects.filter(pk=id).first()
        user_id = request.session.get('user_id')
        recently_shop = [goods.id]
        if user_id:
            shops = request.session.get('re_shop')
            if shops:
                shops.insert(0, goods.id)
                request.session['re_shop'] = shops
            else:
                request.session['re_shop'] = recently_shop

        return render(request, 'detail.html', {'goods': goods})
