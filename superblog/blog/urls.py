from django.contrib import admin
from django.urls import path, include

from blog.views import HomeListView, CategoryListView, AuthorDetailView, post_detail, \
    tag_search, search

urlpatterns = [
    path('', HomeListView.as_view(), name='home'),
    path('post/<str:slug>', post_detail, name='post'),
    path('category/<str:slug>', CategoryListView.as_view(), name='category'),
    path('tag/<str:slug>', tag_search, name='tag'),
    path('author/<str:slug>', AuthorDetailView.as_view(), name='author'),
    path('search/', search, name='search'),
]
