from django.shortcuts import render
from django.views.generic import View, ListView, DetailView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from .models import Movie, Actor, Genre
import json
import requests


class HomeView(View):
    def get(self, *args, **kwargs):
        return render(self.request, "home.html")


class SearchView(View):
    def get(self, *args, **kwargs):
        return render(self.request, "search.html")


class WatchlistView(ListView):
    model = Movie
    paginate_by = 10
    template_name = "watchlist.html"


class MovieDetailView(DetailView):
    model = Movie
    template_name = "movie.html"


def add_movie(request):
    imdbID = json.loads(request.body.decode('utf-8')).get('imdbID')
    movies_qs = Movie.objects.filter(imdbID=imdbID)
    if movies_qs.exists():
        return redirect("watchlist:watchlist")
    else:
        api_key = '6f665eb1'
        url = f'http://www.omdbapi.com/?i={imdbID}&apikey={api_key}'
        response = requests.get(url)
        vals = json.loads(response.text)

        movie = Movie.objects.create(
            imdbID=vals.get('imdbID'),
            title=vals.get('Title'),
        )
        actors = vals.get('Actors').split(',')
        for name in actors:
            actor, created = Actor.objects.get_or_create(name=name)
            movie.actors.add(actor)

        genres = vals.get('Genre').split(',')
        for name in genres:
            genre, created = Genre.objects.get_or_create(name=name)
            movie.genres.add(genre)

        return redirect("watchlist:watchlist")


class MovieDelete(DeleteView):
    model = Movie
    success_url = reverse_lazy('watchlist:watchlist')


def set_watched(request, pk):
    movie = get_object_or_404(Movie, id=pk)
    movie.watched = False if movie.watched else True
    movie.save()
    return redirect("watchlist:watchlist")
