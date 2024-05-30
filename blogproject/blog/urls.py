from .views import *
from django.urls import path


urlpatterns = [
    path('', index, name = "index"),
    path('login/', user_login, name = "login"),
    path('register/', user_register, name = "register"),
    path('logout/', logout_user, name = "logout"),
    path('newblog', createblog, name = "newblog"),
]