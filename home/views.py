from django.shortcuts import render

# Django views
from django.views.generic import TemplateView, DetailView
from django.views.generic import ListView

from db import models

# Time tools
from datetime import datetime

from db.models import Card, Pack

# Q Objects
from django.db.models import Q

# Create your views here.

def all_cards(request):
    pack = models.Pack.objects.all().get(short='FotS')
    card_list = models.Card.objects.all().filter(pack=pack).order_by("code")
    num_cards = len(card_list)
    return render(request, 'home/home.html', {'card_list': card_list, 'card_num': num_cards})


def card(request, code):
    card = models.Card.objects.all().get(code=code)
    return render(request, 'home/single_card.html', {'card': card})

class SearchResultsView(ListView):
    model = Card
    template_name = 'home/home.html'

    def get_queryset(self):
        
        fFaction = models.Faction.objects.all().get(short='lannister')
        fType = models.Type.objects.all().get(name='Plot')
        return Card.objects.filter(Q(faction=fFaction) & Q(type=fType))

