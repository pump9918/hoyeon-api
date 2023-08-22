from django.urls import path
from .views import ProfileListView, ProfileView

app_name = 'users'

urlpatterns = [
    path('list/', ProfileListView.as_view()),
    path('<int:pk>/', ProfileView.as_view()),
]