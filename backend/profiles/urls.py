from django.urls import path
from . import views

app_name = 'profiles'

urlpatterns = [
    path('', views.profile, name='profile'),
    path('login', views.login_user, name='login'),
    path('logout_user', views.logout_user, name='logout'),
    path('registration', views.registration, name='registration'),
    path('settings', views.profile_update, name='settings'),    
]