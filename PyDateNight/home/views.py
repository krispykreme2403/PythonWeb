from typing import Any
from home.models import Business
from django.views.generic import ListView, TemplateView
from home.yelp import YelpController
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib import messages
from string import ascii_uppercase
import re

# Create your views here.

def validate_letter_filter(letter):
    """
    Validate that the letter parameter is a single alphabetic character.
    Returns the validated letter in uppercase, or None if invalid.
    """
    if not letter:
        return None

    # Only allow single alphabetic characters
    if len(letter) == 1 and letter.isalpha():
        return letter.upper()

    return None


class HomeView(TemplateView):
    template_name = 'home.html'


class RestaurantListView(LoginRequiredMixin, ListView):
    model = Business
    template_name = 'restaurant_list.html'
    context_object_name = 'businesses'
    login_url = '/login/'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super(RestaurantListView, self).get_context_data(**kwargs)
        context['alphabet'] = ascii_uppercase
        return context

    def get_queryset(self):
        qs = super(RestaurantListView, self).get_queryset()
        letter = self.request.GET.get('letter', None)
        validated_letter = validate_letter_filter(letter)

        if validated_letter:
            # Use safe string formatting with validated input
            # Django's iregex is safe when the pattern is controlled
            return Business.objects.filter(
                name__iregex=fr'^(?:the )?{re.escape(validated_letter)}.+$'
            ).order_by('-rating', 'location__city')
        return qs.order_by('-rating')


class RestaurantMapView(LoginRequiredMixin, ListView):
    model = Business
    template_name = 'restaurant_map.html'
    context_object_name = 'businesses'
    login_url = '/login/'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super(RestaurantMapView, self).get_context_data(**kwargs)
        context['alphabet'] = ascii_uppercase
        return context

    def get_queryset(self):
        qs = super(RestaurantMapView, self).get_queryset()
        letter = self.request.GET.get('letter', None)
        validated_letter = validate_letter_filter(letter)

        if validated_letter:
            # Use safe string formatting with validated input
            # Django's iregex is safe when the pattern is controlled
            return Business.objects.filter(
                name__iregex=fr'^(?:the )?{re.escape(validated_letter)}.+$'
            ).order_by('-rating', 'location__city')
        return qs.order_by('-rating')


def fetch_restaurant_data(request, location=None):
    yelp = YelpController()
    if location:
        context = {
            'fetch_response': yelp.connect_to_yelp(location=location),
            'alphabet': ascii_uppercase
        }
        return render(request, 'fetch_restaurants.html', context)
    else:
        context = {
            'fetch_response': yelp.connect_to_yelp(),
            'alphabet': ascii_uppercase
        }
        return render(request, 'fetch_restaurants.html', context)


class CustomLoginView(LoginView):
    template_name = 'login.html'

    def get_success_url(self):
        return '/restaurant_list/'

    def form_valid(self, form):
        messages.success(self.request, 'You have successfully logged in!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password.')
        return super().form_invalid(form)
