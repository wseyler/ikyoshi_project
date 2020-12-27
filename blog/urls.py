from blog import views
from django.urls import path

urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),
    path('<slug:slug>/', views.post_detail, name='post_detail'),
]
