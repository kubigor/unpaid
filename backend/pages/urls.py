from django.urls import path
from . import views

app_name = 'pages'

urlpatterns = [
    path('', views.header, name='home'),
    path('newpost', views.create_post, name='newpost'),
    path('search', views.search, name='search'),
    path('inquiry', views.create_inquiry, name='create_inquiry'),
    path('search/results', views.search_results, name='search_results'),
    path('search/<slug:table_name>/<int:page_number>', views.search, name='search'),
    path('<slug:table_name>/<int:product_id>', views.object_detailed, name='object_detailed'),
    path('delete/posts/<int:post_id>/<int:comment_id>', views.delete_comment, name='delete')
]
