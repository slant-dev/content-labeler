from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('articles/', views.articles, name='articles'),
    path('profile/', views.profile, name='profile'),
    path('statistics/', views.statistics, name='statistics'),
]
