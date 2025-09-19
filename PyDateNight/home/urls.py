from django.urls import path, re_path
from django.contrib.auth.views import LogoutView

from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('restaurant_list/', views.RestaurantListView.as_view(),
         name='restaurant_list'),
    path('restaurant_map/', views.RestaurantMapView.as_view(),
         name='restaurant_map'),
    path('fetch_restaurants/', views.fetch_restaurant_data,
         name='fetch_restaurant_data'),
    path('fetch_restaurants/<str:location>/', views.fetch_restaurant_data,
         name='fetch_restaurant_data_with_location')
]
