"""The Cat API testessera extension.

The Cat API (https://thecatapi.com/) is a fun API that provides random cat images and facts. It's commonly used for
testing and demonstrating API integration.

"""
from testessera import RestClient, RestRequest


class ImagesSearchGet(RestRequest):
	def __init__(self, limit : int = 1):
		RestRequest.__init__(self, 'GET', f'/images/search?limit={limit}')


class BreedsGet(RestRequest):
	def __init__(self):
		RestRequest.__init__(self, 'GET', '/breeds')


class BreedGet(RestRequest):
	def __init__(self, breed_id: str):
		RestRequest.__init__(self, 'GET', f'/breeds/{breed_id}')


class TheCatApiClient(RestClient):
	def __init__(self):
		RestClient.__init__(self, base_url='https://api.thecatapi.com/v1')
