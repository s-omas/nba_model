from django.shortcuts import render
from .pull_data import *
# Create your views here.

from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    teams = get_teams()
    print(teams)
    return render(request, 'index.html')
