from collections import deque
from typing import Optional
import logging
import time
import uuid
import json
from confluent_kafka import (
	Consumer,
	Producer,
	Message,
	KafkaError
)
from testessera.json import assert_json


class KafkaConsumer():
	"""Kafka consumer for testing.

	This class encapsulates a Kafka consumer using the `confluent_kafka` library.
	It allows for the consumption and processing of Kafka messages from specified topics.

	Attributes:
		consumer (Consumer): Underlying `confluent_kafka` consumer.
		_topic_queue_mapping (Optional[dict]): Mapping of topic names to queues for
			consuming and processing messages, if provided.

	Args:
		topics (Optional[Union[list[str], dict[str, deque]]]): List of topic names to
			subscribe to, or mapping of topic names to queues for consumption.

	Note:
		If `_topic_queue_mapping` is provided during initialization, the consumer's
		received messages can be added to their respective queues for separate processing.

	Example:
		Initializing with topics list:
		>>> consumer = KafkaConsumer(['topic1', 'topic2'])

		Initializing with topic-queue mapping:
		>>> from collections import deque
		>>> topic_queue_mapping = {'topic1': deque(), 'topic2': deque()}
		>>> consumer = KafkaConsumer(topic_queue_mapping)

	"""
	def __init__(self,
	      		topics: list[str] | dict[str, deque] | None,
			bootstrap_servers=None,
			group_id=None,
			config=None):
		if bootstrap_servers is None:
			bootstrap_servers = 'localhost:9093'
		if group_id is None:
			group_id = f'testattoo-{uuid.uuid4().hex[:8]}'
		if config is None:
			config = {
				"bootstrap.servers": bootstrap_servers,
				"group.id": group_id,
				"default.topic.config": {
					"auto.offset.reset": "latest"
				},
				"max.poll.interval.ms": 86400000,
				"enable.auto.commit": False,
				"enable.partition.eof": True
			}

		self.consumer = Consumer(**config)

		self._topic_queue_mapping = None
		if topics:
			self.subscribe(topics)


	def subscribe(self, topics: list[str] | dict[str, deque]):
		"""Subscribes to `topics` and waits for partition assignment.

		Args:
			topics:	List of topic names to subscribe or mapping of topic names to subscribe to consumption queues.

		Raises:
			KafkaException
		Raises:
			RuntimeError	If called on a closed consumer.

		"""
		try:
			topic_names = list(topics.keys())
			self._topic_queue_mapping = topics
			topics = topic_names
		except AttributeError:
			# `topics` is already a list
			...

		self.consumer.subscribe(topics)
		self._wait_for_partition_assignment()


	def _wait_for_partition_assignment(self):

		# Consider using the on_assign callback provided by confluent_kafka to know when partitions have been assigned

		while True:
			logging.debug('Polling until _PARTITION_EOF')
			msg = self.consumer.poll(0.2)
			if msg:
				error = msg.error()
				if error and error.code() == KafkaError._PARTITION_EOF:	# pylint: disable=protected-access
					break


	def consume_one(self, timeout: float = 300.0) -> Optional[Message]:
		"""Consume and process a single Kafka message.

		This method consumes a single Kafka message and process it. If a message
		is successfully consumed within the given timeout, it is returned. If no message is
		received within the timeout, None is returned.

		Args:
			timeout (float, optional): The maximum time (in seconds) to wait for a message.
				Defaults to 300.0 seconds (5 minutes).

		Returns:
			Optional[Message]: The consumed Kafka message if available, or None if no message
				was received within the timeout.
		"""
		start = time.time()
		while (time.time() - start) < timeout:
			msg = self._poll_iteration()
			if msg:
				return msg

		return None


	def consume_many(self, num_messages: int, timeout: float = 300.0) -> deque[Message]:
		"""Consume and process multiple Kafka messages.

		If the requested number of messages are successfully consumed within
		the timeout, they are returned in a deque. If fewer messages are available before the
		timeout expires, the method returns all available messages.

		If the `_topic_queue_mapping` attribute is provided during initialization,
		the consumed messages will be added to their respective topic-specific queues
		in the `_topic_queue_mapping`. This is useful for scenarios where messages need
		to be processed in a separate queue for each topic.

		Args:
			num_messages (int): The maximum number of messages to consume and process.
			timeout (float, optional): The maximum time (in seconds) to wait for messages.
				Defaults to 300.0 seconds (5 minutes).

		Returns:
			deque[Message]: A deque containing the consumed Kafka messages. The deque may
				contain fewer messages if the timeout expires before the requested number
				of messages are received.
		"""
		msgs = deque()

		start = time.time()
		while ((time.time() - start) < timeout) and (len(msgs) < num_messages):
			msg = self._poll_iteration()
			if msg:
				msgs.appendleft(msg)

		return msgs


	def _poll_iteration(self) -> Optional[Message]:

		msg = self.consumer.poll(1.0)
		if msg:
			error = msg.error()
			if not error:
				if self._topic_queue_mapping:
					topic = msg.topic()
					if topic:
						self._topic_queue_mapping[topic].appendleft(msg)
				return msg
		return None


	def close(self):

		self.consumer.close()


class KafkaProducer():

	def __init__(self, bootstrap_servers: str):

		config = {
			'bootstrap.servers': bootstrap_servers,
			"queue.buffering.max.ms": 0,
			"acks": -1
		}
		self._producer = Producer(config)


	def produce(self, topic, key=None, value=None, partition=-1, timestamp=0, headers=None):
		"""
		
		Raises:
			BufferError
			KafkaException
			NotImplementedError

		"""
		self._producer.produce(topic, key, value, partition, timestamp=timestamp, headers=headers)

		print(f'Flushing message to {topic}')
		self._producer.flush()
		print('Done')


def assert_kafka_message(msg: Message, expected_json_instance=None, expected_json_schema=None, **kwargs):
	"""Asserts the contents of a JSON message consumed from Kafka.

	Args:
		msg:
		expected_json_instance (dict | None):	The expected JSON instance to compare against (optional).
		expected_json_schema (dict | None):	The expected JSON schema to validate against (optional).
		**kwargs (dict):			Additional keyword arguments to compare specific property values. Property names
			should be provided as keys, and expected values as values.

	Raises:
		AssertionError:		Assertion fails.
		JSONDecodeError:	Error decoding the JSON content of the message.
		
	"""
	assert msg, 'No Kafka message provided. If you called consume_one() or consume_many() they timed out.'

	json_instance = json.loads(msg.value())

	assert_json(json_instance, expected_json_instance, expected_json_schema)

	for key, expected_value in kwargs.items():
		actual_value = json_instance[key]
		assert actual_value == expected_value,	\
			f'Expected property `{key}` value was {expected_value} but got value {actual_value}'
