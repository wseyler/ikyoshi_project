# pages/urls.py
from django.urls import path
from .views import HomePageView, AboutPageView
from pages import views

urlpatterns = [
    path('about/', AboutPageView.as_view(), name='about'),
    path('dashboard/', views.user_dashboard, name='user_dashboard'),
    path('', HomePageView.as_view(), name='home'),
    path('signup/', views.signupuser, name='signupuser'),
    path('logout/', views.logoutuser, name='logoutuser'),
    path('login/', views.loginuser, name='loginuser'),
]
