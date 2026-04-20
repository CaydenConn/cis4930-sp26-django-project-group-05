from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('records/', views.movie_list, name='movie_list'),
    path('records/<int:pk>/', views.movie_detail, name='movie_detail'),
    path('records/add/', views.movie_create, name='movie_create'),
    path('records/<int:pk>/edit/', views.movie_update, name='movie_update'),
    path('records/<int:pk>/delete/', views.movie_delete, name='movie_delete'),
    path('weather/', views.weather_list, name='weather_list'),
    path('weather/<int:pk>/', views.weather_detail, name='weather_detail'),
]
