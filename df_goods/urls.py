from django.conf.urls import url,include
from . import views

urlpatterns = [
    url(r'^$',views.index),
    url(r'^list(\d+)_(\d+)_(\d+)/$', views.list_handle),
    url(r'^(\d+)/$',views.detail),
    # 自定义上下文
    url(r'^search/', views.MySearchView()),
]
