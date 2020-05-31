from django.urls import path
from .views import HomeView, SearchView, WatchlistView

app_name = 'watchlist'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('search/', SearchView.as_view(), name='search'),
    path('watchlist/', WatchlistView.as_view(), name='watchlist'),
]
