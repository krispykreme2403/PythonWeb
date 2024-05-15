from typing import Any
from home.models import Business
from django.views.generic import ListView, TemplateView
from home.yelp import YelpController
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from string import ascii_uppercase

# Create your views here.


class HomeView(TemplateView):
    template_name = 'home.html'


class RestaurantListView(LoginRequiredMixin, ListView):
    model = Business
    template_name = 'restaurant_list.html'
    context_object_name = 'businesses'
    login_url = '/admin'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super(RestaurantListView, self).get_context_data(**kwargs)
        context['alphabet'] = ascii_uppercase
        return context

    def get_queryset(self):
        qs = super(RestaurantListView, self).get_queryset()
        letter = self.request.GET.get('letter', None)
        # sort = self.request.Get.get('sort', None)
        print(letter)
        if 'letter' != None:
            return Business.objects.filter(name__iregex=fr'^(?:the )?{letter}.+$').order_by('-rating', 'location__city')


def fetch_restaurant_data(request):
    yelp = YelpController()
    return render(request, 'fetch_restaurants.html', {'fetch_response': yelp.connect_to_yelp(), 'alphabet': ascii_uppercase})
