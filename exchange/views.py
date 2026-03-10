from django.shortcuts import render
from django.views.generic import ListView
from .models import HelpOffer


class HomeView(ListView):
    model = HelpOffer
    template_name = 'exchange/home.html'
    context_object_name = 'Offers'
    
    def get_queryset(self):
        return HelpOffer.objects.select_related('help_request__requester', 'help_request__skill_needed').order_by('-created_at')
    

