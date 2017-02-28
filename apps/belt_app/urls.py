from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^add_user$', views.add_user),
    url(r'^success$', views.success),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^user/(?P<id>\d+)$', views.user),
    url(r'^add_friend/(?P<id>\d+)$', views.add_friend),
    url(r'^delete/(?P<id>\d+)$', views.delete),
    url(r'^delete_user/(?P<id>\d+)$', views.delete_user),
]
