import pytest
from testessera import assert_json


def test_assert_json_instance_success():
	"""Test comparison where JSON instances match. """

	test_json = {'name': 'John', 'age': 30}
	expected_json = {'name': 'John', 'age': 30}

	assert_json(test_json, expected_json_instance=expected_json)


def test_assert_json_instance_failure():
	"""Test comparison where JSON instances do not match. """

	test_json = {'name': 'John', 'age': 30}
	expected_json = {'name': 'Jane', 'age': 25}

	with pytest.raises(AssertionError):
		assert_json(test_json, expected_json_instance=expected_json)


def test_assert_json_schema_success():
	"""Test schema validation where JSON instance matches schema. """

	test_json = {
		'name': 'John',
		'age': 30
	}
	expected_schema = {
		'type': 'object',
		'properties': {
			'name': {
				'type': 'string'
			},
			'age': {
				'type': 'number'
			}
		},
		'required': [
			'name',
			'age'
		]
	}
	assert_json(test_json, expected_json_schema=expected_schema)


def test_assert_json_schema_failure():
	"""Test schema validation where JSON instance doesn't match schema. """

	test_json = {
		'name': 'John',
		'age': 'thirty'
	}
	expected_schema = {
		'type': 'object',
		'properties': {
			'name': {
				'type': 'string'
			},
			'age': {
				'type': 'number'
			}
		},
		'required': [
			'name',
			'age'
		]
	}
	with pytest.raises(AssertionError):
		assert_json(test_json, expected_json_schema=expected_schema)


def test_assert_json_both_parameters_provided():

	with pytest.raises(ValueError):
		assert_json(
			{'name': 'John', 'age': 30},
			expected_json_instance={'name': 'John', 'age': 30},
			expected_json_schema={'type': 'object'}
		)


def test_assert_json_neither_parameter_provided():

	with pytest.raises(ValueError):
		assert_json({'name': 'John', 'age': 30})
