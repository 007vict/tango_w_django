from django.urls import path
from . import views

urlpatterns =[
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('category/<category_name_slug>/', views.category, name='category'),
    path('add_category/', views.add_category, name='add_category'),
    path('category/<category_name_slug>/add_page/', views.add_page, name='add_page'),
]