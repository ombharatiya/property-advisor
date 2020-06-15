"""
Custom user routes and endpoints
"""
from django.urls import path
from .views import home, home_view

urlpatterns = [
    path("", home_view, name="home_view"),
    path("home/", home, name="home"),
    # path("blog/", blog, name="blog"),
]
