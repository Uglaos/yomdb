from django.shortcuts import render
from django.views.generic import View


class HomeView(View):
    def get(self, *args, **kwargs):
        return render(self.request, "home.html")


class SearchView(View):
    def get(self, *args, **kwargs):
        return render(self.request, "search.html")
