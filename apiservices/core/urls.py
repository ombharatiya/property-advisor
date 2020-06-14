"""
Custom user routes and endpoints
"""
from django.urls import path
from .views import home, blog, home_view
from django.views.generic import TemplateView

urlpatterns = [
    path("", home, name="home"),
    path("blog/", blog, name="blog"),
    path("view/", home_view, name="home_view"),
    # path("view/", TemplateView.as_view(template_name = 'home.html')),
    # path('login/', home_view, name = 'login')
]
