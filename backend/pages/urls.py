from django.urls import path
from . import views

app_name = 'pages'

urlpatterns = [
    path('', views.header),
    path('newpost', views.create_post, name='newpost'),
    path('search', views.posts, name='search')
]