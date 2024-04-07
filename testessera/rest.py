import re
import requests
from testessera.json import assert_json


SUCCESS_2XX = 0


class RestRequest():

	def __init__(self, method: str, path: str, body=None, headers=None, query_params=None):

		if headers is None:
			headers = {}
		if query_params is None:
			query_params = {}
		self._method = method
		self._path = path
		self._body = body
		self._headers = headers
		self._query_params = query_params

	@property
	def method(self):

		return self._method

	@property
	def path(self):

		return self._path

	@property
	def headers(self) -> dict:

		return self._headers

	@property
	def query_params(self) -> dict:
		return self._query_params

	@property
	def body(self):

		return self._body

	def __str__(self):
		return f'RestRequest({self.method}, {self.path}, {self.headers}, {self._body})'


class RestClient():
	"""

	Attributes:
		_base_url (str)
		_api_key (str)
		_timeout (float)
		_verify (bool)
		_session (requests.Session)

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
			requests.exceptions	

		TODO: Consider using Request params instead of _build_url()

		"""
		url = self._build_url(rest_request)

		headers = None
		if self._api_key:
			headers = {'X-API-Key': self._api_key}

		request = requests.Request(rest_request.method, url, headers, json=rest_request.json)
		prepared_request = request.prepare()

		return self._session.send(prepared_request, verify=self._verify, timeout=self._timeout)


	def _build_url(self, rest_request: RestRequest) -> str:

		query_params = [f'{param}={value}' for param, value in rest_request.query_params.items()]
		if query_params:
			query_params = '&'.join(query_params)
			url = f'{self._base_url}{rest_request.path}?{query_params}'
		else:
			url = f'{self._base_url}{rest_request.path}'

		return url


def assert_http_response(response: requests.Response, status_code: int, headers=None):
	"""Asserts an HTTP response.

	Args:
		response (requests.Response):
		status_code (int):	Expected status code.
		headers (dict):		Expected headers.

	"""
	assert response.status_code == status_code,	\
		f'Expected status was {status_code} but got status {response.status_code} and response body {response.text}'

	if headers:
		for header, value in headers.items():
			assert response.headers[header].casefold() == value.casefold()


def assert_rest_response(
		response: requests.Response,
		status_code: int = SUCCESS_2XX,
		headers=None,
		json_instance=None,
		json_schema=None):
	"""Asserts a REST response.

	Args:
		response (requests.Response):	Request response.
		status_code (int):		Expected status code.
		headers (Optional[dict]):	Expected headers.
		json_instance (Optional[dict]):	Expected JSON instance.
		json_schema (Optional[dict]):	Expected JSON schema.

	"""
	if status_code:
		assert response.status_code == status_code,	\
			f'Expected status was {status_code} but got status {response.status_code} and response body {response.text}'
	else:
		assert response.status_code // 100 == 2,	\
			f'Expected 2XX status but got status {response.status_code} and response body {response.text}'

	if headers:
		for header, value in headers.items():
			assert response.headers[header].casefold() == value.casefold()

	if json_instance or json_schema:
		# Assert Content-Type is JSON
		content_type = response.headers.get('Content-Type')
		assert content_type == 'application/json' or content_type.startswith('application/json;'),	\
			f'Expected Content-Type application/json but got {content_type}'

		assert_json(response.json(), json_instance, json_schema)


def assert_problem_json_response(
		response: requests.Response,
		status_code: int,
		type: str = '',
		title: str = '',
		detail: str = '',
		instance: str = ''):
	# pylint: disable=too-many-arguments disable=redefined-builtin
	"""Asserts RFC7807 compliant error JSON responses.

	See RFC7807 "Problem Details for HTTP APIs" https://www.rfc-editor.org/rfc/rfc7807.html

	Args:
		status_code (int):	Expected status code.
		type (str):		The exact string to compare with or a regular expression.
		title:			The exact string to compare with or a regular expression.
		detail:			The exact string to compare with or a regular expression.
		instance:		The exact string to compare with or a regular expression.

	"""
	def assert_problem_json_status_code():

		# Assert status code
		assert response.status_code == status_code,	\
			f'Expected status was {status_code} but got status {response.status_code} and response body `{response.text}`'

		# Assert status if present
		status = response_json.get('status')
		if status is not None:
			assert status == status_code

	def assert_problem_json_field(field: str, value: str):

		if value:
			pattern = re.compile(value)
			assert pattern.match(response_json[field])

	response_json = response.json()

	assert_problem_json_status_code()
	assert_problem_json_field('type', type)
	assert_problem_json_field('title', title)
	assert_problem_json_field('detail', detail)
	assert_problem_json_field('instance', instance)
