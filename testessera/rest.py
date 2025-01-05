from typing import Optional
import re
import requests
from testessera.json import assert_json


SUCCESS_2XX = 0
"""int: Used to specify any successful HTTP status code in `assert_rest_response()`. """


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
		"""HTTP method; usually POST, PUT, PATCH or DELETE. """
		return self._method

	@property
	def path(self):
		"""Request URL path. """

		return self._path

	@property
	def headers(self) -> dict:

		return self._headers

	@property
	def query_params(self) -> dict:
		"""Request URL query parameters. """

		return self._query_params

	@property
	def body(self):

		return self._body

	def __str__(self):
		return f'RestRequest({self.method}, {self.path}, {self.headers}, {self._body})'


class Get(RestRequest):
	def __init__(self, path: str, headers=None, query_params=None):
		super().__init__('GET', path, headers=headers, query_params=query_params)


class Post(RestRequest):
	def __init__(self, path: str, body, headers=None, query_params=None):
		super().__init__('POST', path, body, headers, query_params)


class Put(RestRequest):
	def __init__(self, path: str, body, headers=None, query_params=None):
		super().__init__('PUT', path, body, headers, query_params)

class Patch(RestRequest):
	def __init__(self, path: str, body, headers=None, query_params=None):
		super().__init__('PATCH', path, body, headers, query_params)


class Delete(RestRequest):
	def __init__(self, path: str):
		super().__init__('DELETE', path)


class RestClient():
	"""

	Attributes:
		_base_url (str):		REST API base url. E.g. `https://api.thecatapi.com/v1`.
		_api_key (str, optional):	API key.
		_timeout (float):		Timeout passed into `requests` module at every request.
		_verify (bool):
		_session (requests.Session):	Underlaying `requests.Session`.

	"""
	def __init__(self, base_url: str, api_key=None, timeout: int = 20, verify=None):

		self._base_url = base_url
		self._api_key = api_key
		self._timeout = timeout
		self._verify = verify

		self._session = requests.Session()


	def request(self, rest_request: RestRequest) -> requests.Response:
		"""

		The request URL is composed by combining the `_base_url` attribute with
		`RestRequest.path` and `RestRequest.query_params`.

		Raises:
			requests.RequestException

		Note:
			* Consider using Request params instead of _build_url()

		"""
		url = self._build_url(rest_request.path, rest_request.query_params)
		return self._request(rest_request.method, url, rest_request.headers, rest_request.body)


	def get(self, path: str,
			headers: Optional[dict] = None,
			query_params: Optional[dict] = None) -> requests.Response:

		url = self._build_url(path, query_params)
		return self._request('GET', url, headers)


	def post(self, path: str,
			body: dict,
			headers: Optional[dict] = None,
			query_params: Optional[dict] = None) -> requests.Response:
		"""

		Args:
			path (str):			Request path without the base URL. E.g. `/provision`.
			body (dict):			Request body.
			headers (Optional[dict]):	Request headers.
			query_params (Optional[dict]):	Request query parameters.

		"""
		url = self._build_url(path, query_params)
		return self._request('POST', url, headers, body)


	def patch(self, path: str,
			body: dict,
			headers: Optional[dict] = None,
			query_params: Optional[dict] = None) -> requests.Response:

		url = self._build_url(path, query_params)
		return self._request('PATCH', url, headers, body)


	def put(self, path: str,
			body: dict,
			headers: Optional[dict] = None,
			query_params: Optional[dict] = None) -> requests.Response:

		url = self._build_url(path, query_params)
		return self._request('PUT', url, headers, body)


	def delete(self, path: str,
			headers: Optional[dict] = None,
			query_params: Optional[dict] = None) -> requests.Response:

		url = self._build_url(path, query_params)
		return self._request('DELETE', url, headers)


	def _build_url(self, path: str, query_params=None) -> str:

		if query_params:
			query_params = [f'{param}={value}' for param, value in query_params.items()]
			query_params = '&'.join(query_params)
			url = f'{self._base_url}{path}?{query_params}'
		else:
			url = f'{self._base_url}{path}'

		return url


	def _request(self,
			method: str,
			url: str,
			headers: Optional[dict] = None,
			body: Optional[dict] = None) -> requests.Response:

		if self._api_key:
			if headers is None:
				headers = {}
			headers['X-API-Key'] = self._api_key

		request = requests.Request(method, url, headers, json=body)
		prepared_request = request.prepare()

		return self._session.send(prepared_request, verify=self._verify, timeout=self._timeout)


def assert_http_response(response: requests.Response, status_code: int, headers=None):
	"""Asserts an HTTP response.

	Args:
		response (requests.Response):	Response object.
		status_code (int):		Expected status code.
		headers (Optional[dict]):	Expected headers.

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
	"""Asserts RFC9457 compliant error JSON responses.

	RFC9457 defines a "problem detail" to carry machine-readable details of errors in HTTP
	response content to avoid the need to define new error response formats for HTTP APIs.

	Args:
		status_code (int):	Expected status code.
		type (str):		Expected type.
		title (str):		Expected title.
		detail (str):		Expected detail.
		instance (str):		Expected instance.

	Example:
		.. code-block::

			HTTP/1.1 404 Not Found
			Content-Type: application/problem+json
			Content-Language: en

			{
				"type": "https://bookstore.example.com/problems/book-not-found",
				"title": "Book Not Found",
				"status": 404,
				"detail": "The book with ID 12345 could not be found in our database.",
				"instance": "/api/books/12345",
				"timestamp": "2023-11-28T12:34:56Z",
				"custom-field": "Additional information or context here"
			}

	References:
		- RFC9457 "Problem Details for HTTP APIs" https://www.rfc-editor.org/rfc/rfc9457

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
