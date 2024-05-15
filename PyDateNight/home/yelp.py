from requests import Request, Session
from home.models import Business, Category, Coordinates, Location


class YelpController(object):
    _YELP_API_KEY = '7GPm8UQYOVKm0pY31fRuZdKEbv-6lUUbN5inbMocknTUbzqJ3YsFO2_YiOB6QTHz7PV6QBWlSNMQKMdAyAI6pMQAszJQcMJVB381MTcSer_6O5ILZhpSVFzUe2XoY3Yx'
    _URL = 'https://api.yelp.com/v3/businesses/search'
    _HEADERS = {'Authorization': f'Bearer {_YELP_API_KEY}',
                'Content-Type': 'application/json'}

    @classmethod
    def connect_to_yelp(cls, location='Lone Tree, CO', categories='fancy dinner', limit=50):
        params = {'location': location,
                  'categories': categories,
                  'radius': 40000,
                  'limit': limit,
                  'offset': 0,
                  'price': '2,3,4'}
        session = Session()
        request = Request(
            'GET', cls._URL, headers=cls._HEADERS, params=params)
        response_query = Query()
        while params['offset'] < response_query.total and params['offset'] < 900:
            request = Request(
                'GET', cls._URL, headers=cls._HEADERS, params=params)
            response = session.send(request.prepare())
            response_query.add_businesses(response.json())
            params['offset'] += 50
        return 'Success'


class Query(object):
    def __init__(self, response=None):
        self.businesses = []
        self.total = 99999999
        self.region = None

    def add_businesses(self, response):
        M_TO_MILES = 0.000621371
        for business in response['businesses']:
            Location.objects.update_or_create(display_address=' '.join(business['location']['display_address']),
                                              defaults={'address1': business['location']['address1'],
                                                        'address2': business['location']['address2'],
                                                        'address3': business['location']['address3'],
                                                        'city': business['location']['city'],
                                                        'zip_code': business['location']['zip_code'],
                                                        'country': business['location']['country'],
                                                        'state': business['location']['state'],
                                                        'display_address': ' '.join(business['location']['display_address'])})
            for category in business['categories']:
                Category.objects.update_or_create(alias=category['alias'],
                                                  title=category['title'],
                                                  defaults={'alias': category['alias'],
                                                            'title': category['title']})

            Coordinates.objects.update_or_create(latitude=business['coordinates']['latitude'],
                                                 longitude=business['coordinates']['longitude'],
                                                 defaults={'latitude': business['coordinates']['latitude'],
                                                           'longitude': business['coordinates']['longitude']})
            business_result = Business.objects.update_or_create(id=business['id'],
                                                                defaults={'id': business['id'],
                                                                          'alias': business['alias'],
                                                                          'name': business['name'],
                                                                          'image_url': business['image_url'],
                                                                          'is_closed': business['is_closed'],
                                                                          'url': business['url'],
                                                                          'review_count': business['review_count'],
                                                                          'rating': business['rating'],
                                                                          'rating_img_url': f"Review_Ribbon_small_16_{round(business['rating'] * 2) / 2}@2x.png",
                                                                          'price': business['price'],
                                                                          'phone': business['phone'],
                                                                          'display_phone': business['display_phone'],
                                                                          'distance': business['distance'] * M_TO_MILES,
                                                                          'location': Location.objects.get(display_address=' '.join(business['location']['display_address'])),
                                                                          'coordinates': Coordinates.objects.get(latitude=business['coordinates']['latitude'], longitude=business['coordinates']['longitude'])})
            business_result[0].categories.add(*[Category.objects.get(
                alias=category['alias']) for category in business['categories']])
