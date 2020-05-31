from django.shortcuts import render
from django.views.generic import View, ListView
from django.shortcuts import redirect
from .models import Watchlist
from .forms import WatchlistForm


class HomeView(View):
    def get(self, *args, **kwargs):
        return render(self.request, "home.html")


class SearchView(View):
    def get(self, *args, **kwargs):
        return render(self.request, "search.html")


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
        # messages.info(request, "This item was added to your cart")
        return redirect("watchlist:watchlist")
