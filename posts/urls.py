from django.urls import path
from .views import *
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.post_list_create),
]