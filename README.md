# Testessera

Python client classes and advance assertions for testing environments. REST, Kafka and Redis support.

- Tessera (τεσσέρα) - Four, used to refer to the four elements (earth, water, air, fire) or the four cardinal directions (north, south, east, west)
- Test - The means by which the quality of anything is determined.

*Disclaimer: this is a work in progress project, stay tuned for updates.*


## Highlights

- Minimize boilerplate test code and facilitate test code readability.
- Protocols support:
  - HTTP/REST
  - Kafka
  - Redis (coming soon)
- `pytest` smooth integration by instantiating client classes as fixtures.
- Extensible.
  - `RestClient` and `RestRequest` can be derived for customization and minimal initialization (examples soon).


## Getting Started

### Testing a REST Request

E.g. Let's say we are testing a service `orders`.

```python
orders_client = RestClient(base_url='api.orders.test')

response = orders_client.request(
	RestRequest('POST', '/orders', order_payload)
)

assert_rest_response(
	response,
	200,
	expected_json_schema={
		'type': 'object',
		'properties': {
			'order_id': {'type': 'string'},
			'items': {'type': 'array'}
		},
		'required': ['order_id']
	}
)
```

### Testing a Kafka Message Publication

```python

kafka_consumer = KafkaConsumer(topics=['orders'])

response = orders_client.request(
	RestRequest('POST', '/orders', order_payload)
)

msg = kafka_consumer.consume_one(timeout=4.0)

assert_kafka_message(msg, event_type='OrderCreated')

```

## Dependencies

- jsonschema==3.2.0
- requests
- confluent-kafka

<!-- jsonschema==3.2.0
requests==2.31.0
confluent-kafka==2.0.2
redis==4.6.0 -->
