import jsonschema


def assert_json(instance, expected_instance=None, expected_schema=None):
	"""Validates a JSON instance against a expected JSON instance or schema.

	If `expected_instance` is provided, a direct comparison is made.

	If `expected_schema` is provided, the function utilizes `jsonschema` to validate the
	JSON instance against it.

	Args:
		instance (dict or list):	The JSON instance to be asserted.

		expected_instance (dict or list, optional):	The expected JSON instance
			for direct comparison.

		expected_schema (dict, optional):	The JSON schema to validate the instance
			against.

	Raises:
		AssertionError:	The JSON instance doesn't match the expected instance or schema.

	Example:

		# Schema-based validation
		assert_json(
			json_data,
			expected_schema={
				'type': 'object',
				'properties': {
					'name': {'type': 'string'},
					'age': {'type': 'number'}
				},
				'required': ['name']
			}
		)

	"""
	if expected_instance and expected_schema:
		raise ValueError('Provide either `expected_instance` or `expected_schema`, not both')

	if expected_instance:
		assert instance == expected_instance,	\
			f'Expected JSON response body was `{expected_instance}` but got `{instance}`'
	elif expected_schema:
		try:
			jsonschema.validate(instance, expected_schema)
		except jsonschema.ValidationError as e:
			raise AssertionError(f'JSON instance does not match the expected schema. {e}.') from e
	else:
		raise ValueError('Provide expected_instance or expected_schema')
