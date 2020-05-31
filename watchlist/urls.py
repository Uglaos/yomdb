from django.urls import path
from .views import HomeView, SearchView, WatchlistView, add_movie, MovieView

app_name = 'watchlist'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('search/', SearchView.as_view(), name='search'),
    path('search/add/', add_movie, name='add'),
    path('watchlist/', WatchlistView.as_view(), name='watchlist'),
    path('movies/', MovieView.as_view(), name='movies')

]
