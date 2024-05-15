from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('restaurant_list/', views.RestaurantListView.as_view(),
         name='restaurant_list'),
    path('fetch_restaurants/', views.fetch_restaurant_data,
         name='fetch_restaurant_data')
]
