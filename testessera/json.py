import jsonschema


def assert_json(json_instance, expected_json_instance=None, expected_json_schema=None):
	"""Validate JSON instances against expected instances or schemas.
	
	If an `expected_json_instance` is provided, a direct comparison is made against the provided JSON instance. If
	an `expected_json_schema` is provided, the function utilizes `jsonschema` to validate the JSON instance
	against the specified schema.

	Args:
		json_instance (dict or list):	The JSON instance to be validated and asserted.
		expected_json_instance (dict or list, optional):	The expected JSON instance for direct
						comparison.
		expected_json_schema (dict, optional):	The JSON schema to validate the JSON instance against.

	Raises:
		AssertionError		The JSON instance doesn't match the expected instance or schema.

	Example:
		# Schema-based validation
		schema = {
			'type': 'object',
			'properties': {
				'name': {'type': 'string'},
				'age': {'type': 'number'}
			},
			'required': ['name']
		}
		assert_json(json_data, expected_json_schema=schema)

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
