from django.urls import path
from . import views

app_name = 'profiles'

urlpatterns = [
    path('', views.profile, name='profile'),
    path('login', views.login_user, name='login'),
    path('logout_user', views.logout_user, name='logout'),
    path('registration', views.registration, name='registration'),
    path('settings', views.profile_update, name='settings'),
    path('company', views.create_company, name='company'),
    path('type', views.type_option, name='type_option'),
    path('update', views.update_status, name='update_status'),

]