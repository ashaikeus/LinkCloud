from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def card_view(request):
    return render(request, 'card.html')