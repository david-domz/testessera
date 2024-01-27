# Testessera

Python client classes and advance assertions for testing environments. REST, Kafka and Redis support.

- Tessera (τεσσέρα) - Four, used to refer to the four elements (earth, water, air, fire) or the four cardinal directions (north, south, east, west)
- Test - The means by which the quality of anything is determined.

*Disclaimer: this is a work in progress project, stay tuned for updates.*


## Getting Started

Testing a service `orders`.

```python
kafka_consumer = KafkaConsumer(topics=['orders'])

# POST order
response = orders_client.request(
	RestRequest('POST', '/orders', order_payload)
)

# Assert REST response
assert_json_response(response, 200)

assert_json(
	response.json(),
	expected_json_schema={
		'type': 'object',
		'properties': {
			'order_id': {'type': 'string'},
			'items': {'type': 'array'}
		},
		'required': ['order_id']
	}
)

# Assert Kafka message
msg = kafka_consumer.consume_one(timeout=4.0)
assert_kafka_message(msg, event_type='ProvisionCreated')

```

# Dependencies

jsonschema==3.2.0
requests==2.31.0
confluent-kafka==2.0.2
redis==4.6.0
