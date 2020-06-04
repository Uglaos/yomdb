from django.db.models import Q
from django.shortcuts import render
from django.views.generic import View, DetailView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404
from .models import Movie, Actor, Genre
import json
import requests


class HomeView(View):
    def get(self, *args, **kwargs):
        return render(self.request, "home.html")


class SearchView(View):
    def get(self, *args, **kwargs):
        return render(self.request, "search.html")


def is_valid_param(param):
    return param != '' and param is not None


def filter(request):
    qs = Movie.objects.all()
    title_or_actor_query = request.GET.get('title_or_actor')
    genre = request.GET.get('genre')
    watched = request.GET.get('watched')
    not_watched = request.GET.get('not_watched')

    if is_valid_param(title_or_actor_query):
        qs = qs.filter(Q(title__icontains=title_or_actor_query) | Q(actors__name__icontains=title_or_actor_query)).distinct()
    if is_valid_param(genre) and genre != 'Choose...':
        qs = qs.filter(genres__name=genre)
    if watched == 'on':
        qs = qs.filter(watched=True)
    elif not_watched == 'on':
        qs = qs.filter(watched=False)

    return qs


def watchlist(request):
    qs = filter(request)
    context = {
        'movies': qs,
        'genres': Genre.objects.all()
    }
    return render(request, "watchlist.html", context)


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
    success_url = reverse_lazy("watchlist:watchlist")


def set_watched(request, pk):
    movie = get_object_or_404(Movie, id=pk)
    movie.watched = False if movie.watched else True
    movie.save()
    return redirect("watchlist:watchlist")
