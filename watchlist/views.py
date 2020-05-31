from django.shortcuts import render
from django.views.generic import View, ListView
from django.shortcuts import redirect
from django.contrib import messages
from .models import Watchlist, Movie
from .forms import WatchlistForm
import json
import requests


class HomeView(View):
    def get(self, *args, **kwargs):
        return render(self.request, "home.html")


class SearchView(View):
    def get(self, *args, **kwargs):
        return render(self.request, "search.html")


class MovieView(ListView):
    model = Movie
    paginate_by = 10
    template_name = "movies.html"


class WatchlistView(View):
    def get(self, *args, **kwargs):
        form = WatchlistForm()
        watchlists = Watchlist.objects.all()
        context = {
            'form': form,
            'watchlists': watchlists,
        }
        return render(self.request, "watchlist.html", context=context)

    def post(self, *args, **kwargs):
        form = WatchlistForm(self.request.POST or None)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            watchlist = Watchlist.objects.create(name=name)
            message = "New watchlist %s was added to your watchlists" % name
            messages.success(self.request, message)
            return redirect("watchlist:watchlist")


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
        Movie.objects.create(
            imdbID=vals.get('imdbID'),
            title=vals.get('Title'),
            # genre='Genre',
            # actors='Actors'
        )
        return redirect("watchlist:watchlist")
