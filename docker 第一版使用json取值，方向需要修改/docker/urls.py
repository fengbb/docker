from django.conf.urls import include, url
from django.contrib import admin
from dockerweb import views
from dockerweb.views import *

urlpatterns = [
    # Examples:
    # url(r'^$', 'docker.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)), #包括admin django后台管理
    url(r'^$', index), #主页
    url(r'^login',  login),  #登录
    #url(r'^shellinabox/', shellinabox), #暂时不用
    url(r'^logout/',logout), #退出登录
    url(r'^images/json',getImagesJson), #取得images  json数据
    url(r'^containers/json',getContainersJson), #取得images  json数据
    url(r'^images/.*/json$',getImageDetaileJson),
    url(r'^test/',test), #测试 json数据，自己测试用
    url(r'^base/',base), #测试base页面
    url(r'^images/$',images), #images显示页面
    url(r'^images/.*$',imagedetaile),  #显示镜像详情
    url(r'^containers',containers) #images显示页面
    #url(r'^api/v1/pods',pods)
    #url(r'^thtf/', include('thtfl.urls')),
]
