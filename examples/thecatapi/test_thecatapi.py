import pytest
from testessera import assert_rest_response
from testessera_thecatapi import TheCatApiClient, BreedGet


@pytest.fixture(scope='session')
def thecatapi_client():

	yield TheCatApiClient()


def test_get_breed_200_ok(thecatapi_client: TheCatApiClient):
	# pylint: disable=redefined-outer-name
	"""Tests GET /breeds/abyss

	When:
		- breed id is abyss
	Then:
		- Status code 200
		- Response includes id, name, and optionally, origin

	"""
	response = thecatapi_client.request(BreedGet(breed_id='abys'))

	assert_rest_response(
		response,
		200,
		json_schema={
			'type': 'object',
			'properties': {
				'id': {'type': 'string'},
				'name': {'type': 'string'},
				'origin': {'type': 'string'}
			},
			'required': ['id', 'name']
		}
	)


def test_get_breed_400_invalid_data(thecatapi_client: TheCatApiClient):
	# pylint: disable=redefined-outer-name

	response = thecatapi_client.request(BreedGet(breed_id='invalid'))

	assert_rest_response(response, 400)
