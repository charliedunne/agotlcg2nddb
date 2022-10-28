from django.urls import path
from . import views
from .views import SearchResultsView

urlpatterns = [
    path('home', views.all_cards, name='cardList'),
    path('home/<code>/', views.card, name='singlecard'),
    path('search', SearchResultsView.as_view(), name='search')
]