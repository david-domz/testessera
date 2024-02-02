import pytest
from testessera import assert_rest_response
from thecatapi import TheCatApiClient, BreedGet


@pytest.fixture(scope='session')
def thecatapi_client():

	yield TheCatApiClient()


def test_get_breed(thecatapi_client: TheCatApiClient):
	# pylint: disable=redefined-outer-name

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