from django.urls import path
from . import views

urlpatterns = [
    path('lgoin/', views.user_login, name='public_user_login'),
    path('register/', views.user_register, name='public_user_register'),
    path('logout/', views.user_logout, name='public_user_logout'),
    path('book-software/', views.book, name='book'),
]