# blog/urls.py

from django.urls import path
from .views import home, post_create, post_edit, post_delete, register, loginPage, logoutUser, post_detail, posts_by_category

urlpatterns = [
    path('', home, name='home'),
    path('post/new/', post_create, name='post_create'),
    path('post/edit/<int:pk>/', post_edit, name='post_edit'),
    path('post/delete/<int:pk>/', post_delete, name='post_delete'),
    path('register/', register, name='register'),
    path('login/', loginPage, name='login'),
    path('logout/', logoutUser, name='logout'),
    path('post/<int:pk>/', post_detail, name='post_detail'),
    path('category/<int:category_id>/', posts_by_category, name='posts_by_category'),
]
