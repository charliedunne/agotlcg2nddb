from django.urls import path
from . import views

urlpatterns = [
    path('home', views.all_cards, name='cardList'),
    path('home/<code>/', views.card, name='singlecard'),
]