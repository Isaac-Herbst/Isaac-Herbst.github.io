from django.urls import path
# here we are importing all the Views from the views.py file
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('new_chat/', views.new_chat, name='new_chat'),
    path('error-handler/', views.error_handler, name='error_handler'),
    path('download_file/', views.download_file, name='download_file'),
    path('user_profile/', views.user_profile, name='user_profile'),
]