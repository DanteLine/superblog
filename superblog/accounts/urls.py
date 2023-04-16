from django.urls import path
from django.contrib.auth import views

from .views import registration, userlogin, user_logout, simple_user, \
    update_user_author, add_post, postupdate, postdelete

urlpatterns = [
    path('add-news', add_post, name='add_post'),
    path('login/', userlogin, name='login'),
    path('register/', registration, name='register'),
    path('logout/', user_logout, name='logout'),
    path('<str:username>', simple_user, name='lk'),
    path('update_user/<str:username>/', update_user_author, name='add_author_info'),
    path('update_post/<str:slug> ', postupdate, name='update_post'),
    path('delete/<str:slug>', postdelete, name='delete_post'),
]
