from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('signup/', views.user_signup, name = "user_signup"),
    path('logout/', views.logout_view, name = "logout_view"),
    path('login/', views.login_view, name = "login_view"),
    path('user/<int:pk>/', views.post_detail, name='profile_detail'),
]
