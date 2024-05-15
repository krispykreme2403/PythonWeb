from django.db import models
from django.contrib.auth.models import User
from math import radians, cos, sin, asin, sqrt


class UserLocation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address1 = models.CharField(max_length=100, null=True)
    address2 = models.CharField(max_length=100, null=True, blank=True)
    address3 = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True)
    zip_code = models.CharField(max_length=10, null=True)
    country = models.CharField(max_length=100, null=True)
    state = models.CharField(max_length=100, null=True)
    display_address = models.CharField(max_length=250, null=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=8, null=True)
    longitude = models.DecimalField(max_digits=11, decimal_places=8, null=True)


class Location(models.Model):
    address1 = models.CharField(max_length=100, null=True)
    address2 = models.CharField(max_length=100, null=True)
    address3 = models.CharField(max_length=100, null=True)
    city = models.CharField(max_length=100, null=True)
    zip_code = models.CharField(max_length=10, null=True)
    country = models.CharField(max_length=100, null=True)
    state = models.CharField(max_length=100, null=True)
    display_address = models.CharField(max_length=250, null=True)


class Category(models.Model):
    alias = models.CharField(max_length=100)
    title = models.CharField(max_length=100)


class Coordinates(models.Model):
    latitude = models.DecimalField(max_digits=10, decimal_places=8)
    longitude = models.DecimalField(max_digits=11, decimal_places=8)


class Business(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    alias = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    image_url = models.CharField(max_length=250)
    is_closed = models.BooleanField()
    url = models.CharField(max_length=250)
    review_count = models.IntegerField()
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    rating_img_url = models.CharField(
        max_length=250, default="Review_Ribbon_small_16_0.0@2x.png")
    price = models.CharField(max_length=10, null=True)
    phone = models.CharField(max_length=20)
    display_phone = models.CharField(max_length=20)
    distance = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.ForeignKey(
        Location, on_delete=models.CASCADE, null=True)
    categories = models.ManyToManyField(Category)
    coordinates = models.ForeignKey(
        Coordinates, on_delete=models.CASCADE, null=True)


def calculate_travel_distance(lon1, lat1, lon2, lat2):
    """
    Calculate the distance between two points on earth (Bird's flight distance) in miles
    :param lon1: longitude of first point
    :param lat1: latitude of first point
    :param lon2: longitude of second point
    :param lat2: latitude of second point
    :return: distance between two points in miles
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(
        radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1  # change in longitude
    dlat = lat2 - lat1  # change in latitude
    a = sin(dlat/2)**2 + cos(lat1) * \
        cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 3956  # Radius of earth in miles

    return c * r
