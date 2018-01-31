from django.conf.urls import url
from . import views

urlpatterns = [
    url(r"^$",views.cart),
    url(r'^(\d+)/(\d+)/$',views.cart_handle),
    url(r'^edit/(\d+)/(\d+)/$',views.edit),
    url(r'^del/(\d+)/$',views.delete),
]