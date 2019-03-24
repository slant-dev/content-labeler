from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('articles/', views.articles, name='articles'),
    path('profile/', views.profile, name='profile'),
    path('statistics/', views.statistics, name='statistics'),
    path('label/articles/', views.label_articles, name='label_articles'),
    path('label/sentences/', views.label_sentences, name='label_sentences'),
]
