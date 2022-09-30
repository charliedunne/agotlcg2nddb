from django.shortcuts import render

# Django views
from django.views.generic import TemplateView, DetailView

from db import models

# Time tools
from datetime import datetime

from db.models import Card

# Create your views here.

def all_cards(request):
    card_list = models.Card.objects.all()
    return render(request, 'home/home.html', {'card_list': card_list})


def card(request, code):
    card = models.Card.objects.all().get(code=code)
    return render(request, 'home/single_card.html', {'card': card})


