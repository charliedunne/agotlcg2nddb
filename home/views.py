from django.shortcuts import render

# Django views
from django.views.generic import TemplateView

# Time tools
from datetime import datetime

# Create your views here.

class HomeView(TemplateView):
    template_name = 'home/home.html'
    extra_context = {'today': datetime.today()}