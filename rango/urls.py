from django.urls import path
from . import views

urlpatterns =[
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('category/<category_name_slug>/', views.category, name='category'),
    path('add_category/', views.add_category, name='add_category'),
    path('category/<category_name_slug>/add_page/', views.add_page, name='add_page'),
    # path('register/', views.register, name='register'),
    # path('login/', views.user_login, name='login')
    # path('logout/', views.user_logout, name='logout'),
    path('restricted/', views.restricted, name='restricted'),
    path('goto/', views.track_url, name='goto'),
    path('add_profile/', views.profile_registration, name='profile_registration'),
    # path('profile/', views.profile, name='profile'),
    path('like_category/', views.like_category, name='like_category'),
]