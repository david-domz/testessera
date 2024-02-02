import jsonschema


def assert_json(json_instance, expected_json_instance=None, expected_json_schema=None):
	"""Validates JSON instances against expected instance or schema.

	If `expected_json_instance` is provided, a direct comparison is made.

	If `expected_json_schema` is provided, the function utilizes `jsonschema` to validate the
	JSON instance against it.

	Args:
		json_instance (dict or list):	The JSON instance to be asserted.

		expected_json_instance (dict or list, optional):	The expected JSON instance
			for direct comparison.

		expected_json_schema (dict, optional):	The JSON schema to validate the instance
			against.

	Raises:
		AssertionError:	The JSON instance doesn't match the expected instance or
			schema.

	Example:

		# Schema-based validation
		assert_json(
			json_data,
			expected_json_schema={
				'type': 'object',
				'properties': {
					'name': {'type': 'string'},
					'age': {'type': 'number'}
				},
				'required': ['name']
			}
		)

	"""
	if expected_json_instance and expected_json_schema:
		assert ValueError('Provide only expected_json_instance or expected_json_schema, not both.')

	if expected_json_instance:
		assert json_instance == expected_json_instance,	\
			f'Expected JSON response body was `{expected_json_instance}` but got `{json_instance}`'
	elif expected_json_schema:
		try:
			jsonschema.validate(json_instance, expected_json_schema)
		except jsonschema.ValidationError as e:
			raise AssertionError('JSON instance does not match the expected JSON schema') from e
