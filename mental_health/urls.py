# personal_blog/urls.py

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.home, name="home"), #path to home page
    path("login/", views.user_login, name="login"), #path to authentication
    path('logout/', views.user_logout, name='logout'),
    path("register/", views.register, name="register"), #path to registration
    path("admin/", admin.site.urls, name="admin"),
    path("", include("blog.urls")),
    path("", include("dashboard.urls")),
    path("", include("Chat.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)