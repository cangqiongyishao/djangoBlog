from django.urls import path

from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.index, name='index'),
    path('blog/<blog_id>', views.blog_detail, name='blog_detail')

]
