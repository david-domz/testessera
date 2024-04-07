import pytest
from testessera import assert_json


def test_assert_instance_expected_instance_success():

	instance = {'name': 'John', 'age': 30}
	expected_instance = {'name': 'John', 'age': 30}

	assert_json(instance, expected_instance=expected_instance)


def test_assert_instance_expected_instance_failure():

	instance = {'name': 'John', 'age': 30}
	expected_instance = {'name': 'Jane', 'age': 25}

	with pytest.raises(AssertionError):
		assert_json(instance, expected_instance=expected_instance)


def test_assert_json_expected_schema_success():

	instance = {
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
	assert_json(instance, expected_schema=expected_schema)


def test_assert_json_expected_schema_failure():

	instance = {
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
		assert_json(instance, expected_schema=expected_schema)


def test_assert_json_value_error_both_parameters_provided():

	with pytest.raises(ValueError):
		assert_json(
			{'name': 'John', 'age': 30},
			expected_instance={'name': 'John', 'age': 30},
			expected_schema={'type': 'object'}
		)


def test_assert_json_value_error_neither_parameter_provided():

	with pytest.raises(ValueError):
		assert_json({'name': 'John', 'age': 30})
