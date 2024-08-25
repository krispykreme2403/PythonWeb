from requests import Request, Session
from home.models import Business, Category, Coordinates, Location


class YelpController(object):
    _YELP_API_KEY = '7GPm8UQYOVKm0pY31fRuZdKEbv-6lUUbN5inbMocknTUbzqJ3YsFO2_YiOB6QTHz7PV6QBWlSNMQKMdAyAI6pMQAszJQcMJVB381MTcSer_6O5ILZhpSVFzUe2XoY3Yx'
    _URL = 'https://api.yelp.com/v3/businesses/search'
    _HEADERS = {'Authorization': f'Bearer {_YELP_API_KEY}',
                'Content-Type': 'application/json'}
    _GRAPHQL_URL = 'https://api.yelp.com/v3/graphql'
    _GRAPHQL_HEADERS = {'Authorization': f'Bearer {_YELP_API_KEY}',
                        'Content-Type': 'application/graphql'}

    @classmethod
    def connect_to_yelp(cls, location='Centennial, CO', term='date night', categories='restaurants,All', limit=50, offset=0):
      '''
      Connects to the Yelp API and retrieves businesses based on the search parameters
      :param location: str
      :param term: str
      :param categories: str
      :param limit: int
      :param offset: int
      :return: str

      Towns to Search:
      Denver, CO
      Highlands Ranch, CO
      Littleton, CO
      Aurora, CO
      Lakewood, CO
      Lone Tree, CO
      Parker, CO
      Castle Rock, CO
      Englewood, CO
      Centennial, CO

      Categories:
      restaurants,All

      Term:
      date night

      
      '''




      session = Session()
      response_query = Query()
      while True:
            GRAPHQL_QUERY = f'''query MyQuery {{
  search(
    categories: "{categories}"
    location: "{location}"
    limit: {limit}
    offset: {offset}
    price: "2,3,4"
    radius: 8000
  ) {{
    total
    business {{
      id
      alias
      coordinates {{
        latitude
        longitude
      }}
      name
      is_closed
      price
      phone
      photos
      url
      rating
      location {{
        address1
        address3
        address2
        city
        country
        formatted_address
        postal_code
        state
      }}
      categories {{
        alias
        title
      }}
      distance
      display_phone
      review_count
    }}
  }}
}}'''
            response = session.request('POST', cls._GRAPHQL_URL, headers=cls._GRAPHQL_HEADERS, data=GRAPHQL_QUERY)
            response_json = response.json()['data']['search']
            if response.status_code == 200:
                if len(response_json['business']) == 0:
                    return f'Success: Added/Updated {response_json["total"]} businesses'
                response_query.add_businesses(response_json)
                offset += limit
            else:
                return f'Error: {response.status_code} -> {response.json()['error']['description']}'


class Query(object):
    def __init__(self, response=None):
        self.businesses = []
        self.total = 99999999
        self.region = None

    def add_businesses(self, response):
        M_TO_MILES = 0.000621371
        self.total = response['total']
        for business in response['business']:
            Location.objects.update_or_create(display_address=business['location']['formatted_address'],
                                              defaults={'address1': business['location']['address1'],
                                                        'address2': business['location']['address2'],
                                                        'address3': business['location']['address3'],
                                                        'city': business['location']['city'],
                                                        'zip_code': business['location']['postal_code'],
                                                        'country': business['location']['country'],
                                                        'state': business['location']['state'],
                                                        'display_address': business['location']['formatted_address']})
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
                                                                          'image_url': business['photos'][0],
                                                                          'is_closed': business['is_closed'],
                                                                          'url': business['url'],
                                                                          'review_count': business['review_count'],
                                                                          'rating': business['rating'],
                                                                          'rating_img_url': f"Review_Ribbon_small_16_{round(business['rating'] * 2) / 2}@2x.png",
                                                                          'price': business['price'],
                                                                          'phone': business['phone'],
                                                                          'display_phone': business['display_phone'],
                                                                          'distance': business['distance'] * M_TO_MILES,
                                                                          'location': Location.objects.get(display_address=business['location']['formatted_address']),
                                                                          'coordinates': Coordinates.objects.get(latitude=business['coordinates']['latitude'], longitude=business['coordinates']['longitude'])})
            business_result[0].categories.add(*[Category.objects.get(
                alias=category['alias']) for category in business['categories']])
