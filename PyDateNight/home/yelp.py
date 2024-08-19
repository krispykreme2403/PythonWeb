from requests import Request, Session
from home.models import Business, Category, Coordinates, Location


class YelpController(object):
    _YELP_API_KEY = '7GPm8UQYOVKm0pY31fRuZdKEbv-6lUUbN5inbMocknTUbzqJ3YsFO2_YiOB6QTHz7PV6QBWlSNMQKMdAyAI6pMQAszJQcMJVB381MTcSer_6O5ILZhpSVFzUe2XoY3Yx'
    _URL = 'https://api.yelp.com/v3/businesses/search'
    _HEADERS = {'Authorization': f'Bearer {_YELP_API_KEY}',
                'Content-Type': 'application/json'}

    @classmethod
    def connect_to_yelp(cls, location='Englewood, CO', term='date night', categories='restaurants,All', limit=50):
        params = {'location': location,
                  'term': term,
                  'categories': categories,
                  'radius': 30000,
                  'limit': limit,
                  'offset': 0,
                  'price': '2,3,4'}
        session = Session()
        response_query = Query()
        while True:
            response = session.request('GET', cls._URL, headers=cls._HEADERS, params=params)
            if response.status_code == 200:
                response_query.add_businesses(response.json())
                params['offset'] += limit
            elif response.status_code == 400:
                response_description = response.json()['error']['description']
                if response_description.startswith('Too many results requested, limit+offset'):
                    params['offset'] = int(response_description[52:len(response_description) - 1]) - limit
                    response = session.request('GET', cls._URL, headers=cls._HEADERS, params=params)
                    response_query.add_businesses(response.json())
                    break
                else:
                    return f'Error: {response.status_code} -> {response.json()['error']['description']}'
            else:
                return f'Error: {response.status_code} -> {response.json()['error']['description']}'
        return 'Success'


class Query(object):
    def __init__(self, response=None):
        self.businesses = []
        self.total = 99999999
        self.region = None

    def add_businesses(self, response):
        M_TO_MILES = 0.000621371
        self.total = response['total']
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
