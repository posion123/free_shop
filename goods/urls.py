from django.urls import path

from fresh_shop.settings import MEDIA_URL, MEDIA_ROOT
from goods import views
urlpatterns = [
    path('index/', views.index, name='index'),
    path('cart/', views.cart, name='cart'),
    path('detail/<int:id>', views.detail, name='detail'),

]
