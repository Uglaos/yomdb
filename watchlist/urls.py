from django.urls import path
from .views import HomeView, SearchView, add_movie, MovieDetailView, MovieDelete, set_watched, watchlist

app_name = 'watchlist'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('search/', SearchView.as_view(), name='search'),
    path('search/add/', add_movie, name='add'),
    path('watchlist/', watchlist, name='watchlist'),
    path('movie/<int:pk>/', MovieDetailView.as_view(), name='movie'),
    path('delete/<int:pk>/', MovieDelete.as_view(), name='delete'),
    path('watched/<int:pk>/', set_watched, name='set_watched'),
]
