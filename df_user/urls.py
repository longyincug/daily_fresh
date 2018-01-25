from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^register/$',views.df_register),
    url(r'^registerHandle/$',views.df_register_handle),
    url(r'^login/$',views.df_login),

]