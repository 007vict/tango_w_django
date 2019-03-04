from django.urls import path
from django.contrib import admin
from .views import searchposts, searchcategory

app_name = 'search'

urlpatterns = [
    path('', searchposts, name='searchposts'),
    path('category/', searchcategory, name='searchcategory'),

]
