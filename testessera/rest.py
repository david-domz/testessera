import re
import requests
from testessera.json import assert_json


class RestRequest():

	def __init__(self, verb: str, path: str, json_data: dict = None):

		self._verb = verb
		self._path = path
		self._headers = {}
		self._json_data = json_data

	@property
	def verb(self):

		return self._verb

	@property
	def path(self):

		return self._path

	@property
	def headers(self):

		return self._headers

	@property
	def json(self):

		return self._json_data



class RestClient():
	"""

	Attributes:

		_base_url (str)
		_api_key
		_timeout (float)

	"""

	def __init__(self, base_url: str, api_key=None, timeout: int = 60, verify=None):

		self._base_url = base_url
		self._api_key = api_key
		self._timeout = timeout
		self._verify = verify

		self._session = requests.Session()



	def request(self, rest_request: RestRequest) -> requests.Response:
		"""

		Raises:
			requests.exceptions.SSLError:	Unable to verify the certificate
			requests.exceptions.ConnectTimeout

		"""
		url = f'{self._base_url}{rest_request.path}'

		headers = None
		if self._api_key:
			headers = {'X-API-Key': self._api_key}

		return self._request(rest_request.verb, url, headers=headers, json_data=rest_request.json)


	def _request(self, method, url, headers=None, json_data=None) -> requests.Response:

		request = requests.Request(method, url, headers, json=json_data)
		prepared_request = request.prepare()

		return self._session.send(prepared_request, verify=self._verify, timeout=self._timeout)


def assert_response(
		response: requests.Response,
		status_code: int,
		headers: dict | None = None):

	assert response.status_code == status_code,	\
		f'Expected status was {status_code} but got status {response.status_code} and response body `{response.text}`'

	if headers:
		for header, value in headers.items():
			assert response.headers[header].casefold() == value.casefold()


def assert_json_response(
		response: requests.Response,
		status_code: int,
		json_instance=None,
		json_schema=None):

	assert_response(response, status_code)


	if response.text:
		content_type = response.headers.get('Content-Type')
		assert content_type == 'application/json' or content_type.startswith('application/json;')

		assert_json(response.json(), json_instance, json_schema)


def assert_problem_json_response(
		response: requests.Response,
		status_code: int,
		type_: str | None = None,
		title: str | None = None,
		detail: str | None = None,
		instance: str | None = None):
	# pylint: disable=too-many-arguments
	"""Asserts RFC7807 compliant error JSON responses.

	See RFC7807 "Problem Details for HTTP APIs" https://www.rfc-editor.org/rfc/rfc7807.html

	Args:
		status_code:	Expected status code.
		type_:		It can be the exact string to compare with or a regular expression.
		title:		It can be the exact string to compare with or a regular expression.
		detail:		It can be the exact string to compare with or a regular expression.
		instance	It can be the exact string to compare with or a regular expression.

	"""
	def assert_problem_json_status_code():

		# Assert HTTP status code
		assert response.status_code == status_code,	\
			f'Expected status was `{status_code}` but got status `{response.status_code}` and response body `{response.text}`'

		# Assert `status` field if present
		status = response_json.get('status')
		if status is not None:
			assert status == status_code

	def assert_problem_json_field(field: str, value: str | None = None):
		# Assert str field
		if value is not None:
			pattern = re.compile(value)
			assert pattern.match(response_json[field])

	response_json = response.json()

	assert_problem_json_status_code()
	assert_problem_json_field('type', type_)
	assert_problem_json_field('title', title)
	assert_problem_json_field('detail', detail)
	assert_problem_json_field('instance', instance)


def assert_request_response(
		rest_client: RestClient,
		rest_request: RestRequest,
		status_code: int,
		headers: dict | None = None):

	response = rest_client.request(rest_request)

	assert_response(response, status_code, headers)


def assert_request_json_response(
		rest_client: RestClient,
		rest_request: RestRequest,
		status_code: int,
		headers: dict | None = None,
		json_instance=None,
		json_schema=None):

	response = rest_client.request(rest_request)

	assert_json_response(response, status_code, json_instance, json_schema)
