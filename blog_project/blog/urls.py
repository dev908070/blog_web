from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import *

urlpatterns = [
    path('',home,name='home'),
    path('login/', custom_login, name='login'),
    path('logout/', custom_logout, name='logout'),
    path('signup/',signup, name='signup'),
    
    path('blog_list/', views.blog_list, name='blog_list'),
    path('blog_detail/<int:pk>/', views.blog_detail, name='blog_detail'),
    path('share_blog/<int:blog_id>/share/', views.share_blog, name='share_blog'),
    path('blog/<int:blog_id>/like/', like_blog, name='like_blog'),

]
