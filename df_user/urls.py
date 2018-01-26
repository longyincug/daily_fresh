from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^register/$',views.df_register),
    url(r'^registerHandle/$',views.df_register_handle),
    url(r'^login/$',views.df_login),
    url(r'^login_handle/$',views.df_login_handle),
    url(r'^info/$',views.user_info),
    url(r'^user_info/$',views.user_info),
    url(r'^user_site/$',views.user_site),
    url(r'^user_order/$',views.user_order),
    url(r'^site_handle/$',views.site_handle),

]