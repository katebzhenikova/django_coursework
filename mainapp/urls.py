from django.urls import path
from django.contrib import admin
from mainapp.views import BlogCreateView, BlogListView, BlogDetailView, \
    BlogUpdateView, BlogDeleteView, toggle_activity
from django.views.decorators.cache import cache_page

from mainapp.apps import MainappConfig

app_name = MainappConfig.name

urlpatterns = [

    path('blog_form_create/', BlogCreateView.as_view(), name='blog_form_create'),
    path('', cache_page(60)(BlogListView.as_view()), name='blog_list'),
    path('<int:pk>/blog_detail/', BlogDetailView.as_view(), name='blog_detail'),
    path('<int:pk>/blog_form/', BlogUpdateView.as_view(), name='blog_form'),
    path('<int:pk>/blog_confirm_delete/', BlogDeleteView.as_view(), name='blog_confirm_delete'),
    path('<int:pk>/activity/', toggle_activity, name='toggle_activity'),

]

