from .views import *
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
    path('', index, name = "index"),
    path('login/', user_login, name = "login"),
    path('register/', user_register, name = "register"),
    path('logout/', LogoutView.as_view(next_page='/login/'), name='logout'),
    path('newblog/', createblog, name = "newblog"),
    path('individual/', search_title, name = "individual"),
    path('<int:pk>/details/', blog_details, name = "details"),
    path('<int:pk>/edit/', edit_blog, name = "edit"),
    path('<int:pk>/delete/', delete_blog, name = "delete"),
    path('myblog/', my_blogs, name = "myblog"),
    path('privateblog/', private_blog, name = "privateblog"),
]