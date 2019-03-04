from django.urls import path
from django.contrib import admin
from .views import (searchposts)

app_name = 'search'

urlpatterns = [
     path('', searchposts, name='searchposts'),

]
