from django.urls import path
from . import views

urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),
    path("profile/", views.user_profile, name="profile"),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('book_appointment/', views.book_appointment, name='book_appointment'),
    path('view_appointment/', views.view_appointments, name='view_appointment'),
]