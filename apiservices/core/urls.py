"""
Custom user routes and endpoints
"""
from django.urls import path
from .views import home, blog


urlpatterns = [
    path("", home, name="home"),
    path("blog/", blog, name="blog"),
]
