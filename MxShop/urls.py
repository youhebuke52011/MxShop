"""MxShop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from django.conf.urls import url, include
from django.views.static import serve
from rest_framework.routers import DefaultRouter
import xadmin

# from goods.view_base import GoodsListView
# from goods.views import GoodListView
from goods.views import GoodListViewSet, CategoryViewset
from user.views import SmsCodeViewset, UserViewSet
from MxShop.settings import MEDIA_ROOT
from rest_framework.authtoken import views
from rest_framework_jwt.views import obtain_jwt_token

router = DefaultRouter()

router.register(r'goods', GoodListViewSet, base_name="goods")
router.register(r'categorys', CategoryViewset, base_name="categorys")
router.register(r'codes', SmsCodeViewset, base_name="codes")
router.register(r'users', UserViewSet, base_name="users")


urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    # url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),

    # drf自带的token认证模式
    url(r'^api-auth/', include('rest_framework.urls')),

    # url(r'^goods/$', GoodsListView.as_view()),
    # url(r'^goods/$', GoodListView.as_view()),
    # url(r'^goods/$', good_list, name="good-list"),
    url(r'^', include(router.urls)),
    # drf自带token认证
    # url(r'^api-token-auth/', views.obtain_auth_token),
    # jwt认证
    url(r'^login/', obtain_jwt_token),

]
