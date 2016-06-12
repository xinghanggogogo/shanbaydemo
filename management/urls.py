# -*- coding:utf-8 -*-
#为每一个app定义一个路由
from django.conf.urls import url
from management import views

urlpatterns = [
    url(r'^$', views.index, name='homepage'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^set_password/$', views.set_password, name='set_password'),
    url(r'^add_book/$', views.add_book, name='add_book'),
    url(r'^add_img/$', views.add_img, name='add_img'),
    url(r'^view_book_list/$', views.view_book_list, name='view_book_list'),
    url(r'^view_book/detail/$', views.detail, name='detail'),
    url(r'^sub_comment/$', views.sub_comment, name='sub_comment'),
    url(r'^wordslist/$',views.wordslist,name='wordslist'),
    url(r'^worddetail/$', views.worddetail, name='worddetail'),
    url(r'^sub_comment2/$', views.sub_comment2, name='sub_comment2'),
    url(r'^setflag/$', views.setflag, name='setflag'),
    url(r'^nextone/$', views.nextone, name='nextone'),
    url(r'^numerror/$', views.numerror, name='numerror'),
]