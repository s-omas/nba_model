from django.shortcuts import render
from .pull_data import *
from .models import Team

# Create your views here.

from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return render(request, 'index.html')

def teams(request):
    return render(request, 'teams.html',  {'teams': Team.objects.all()})