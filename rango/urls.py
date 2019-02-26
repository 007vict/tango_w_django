from django.urls import path, re_path
from . import views
from django.conf.urls import url

urlpatterns =[
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    re_path(r'^category/(?P<category_name_slug>[\w\-]+)/$', views.category, name='category')
]