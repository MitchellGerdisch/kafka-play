# Based on this blog: https://help.aiven.io/en/articles/489572-getting-started-with-aiven-kafka
from kafka import KafkaConsumer, KafkaProducer, KafkaAdminClient
import kafka
import ssl
import os
from kafka_creds import KafkaCreds
#import logging
#logging.basicConfig(level=logging.DEBUG)

creds = KafkaCreds()

#try:

# Get credentials for interacting with Kafka cluster
BOOTSTRAP_SERVERS = creds.bootstrap_servers
USER = creds.user
PASSWORD = creds.password
CA_FILE = creds.ca_file
CERT_FILE = creds.cert_file
KEY_FILE = creds.key_file

'''
# Create topic
admin = KafkaAdminClient(    
	bootstrap_servers=BOOTSTRAP_SERVERS,
    security_protocol="SSL",
    ssl_cafile=CA_FILE,
    ssl_certfile=CERT_FILE,
    ssl_keyfile=KEY_FILE
)

admin.create_topics([
	{ 
		"name":"mitchtest",
		"num_partitions": 1,
		"replication_factor": 1
	}],validate_only=True)

'''

# Start producing data and filling the stream

# Create instance of a producer
producer = KafkaProducer(
    bootstrap_servers=BOOTSTRAP_SERVERS,
    security_protocol="SSL",
    ssl_cafile=CA_FILE,
    ssl_certfile=CERT_FILE,
    ssl_keyfile=KEY_FILE
)

for i in range(1, 4):
    message = "message number {}".format(i)
    print("Sending: {}".format(message))
    producer.send("demo-topic", message.encode("utf-8"))

# Force sending of all messages

producer.flush()

# This script receives messages from a Kafka topic


consumer = KafkaConsumer(
    "demo-topic",
    auto_offset_reset="earliest",
    client_id="demo-client-1",
    group_id="demo-group",
    security_protocol="SSL",
    bootstrap_servers=BOOTSTRAP_SERVERS,
    ssl_cafile=CA_FILE,
    ssl_certfile=CERT_FILE,
    ssl_keyfile=KEY_FILE
)

# Call poll twice. First call will just assign partitions for our
# consumer without actually returning anything

for _ in range(2):
    raw_msgs = consumer.poll(timeout_ms=1000)
    for tp, msgs in raw_msgs.items():
        for msg in msgs:
            print("Received: {}".format(msg.value))

# Commit offsets so we won't get the same messages again

consumer.commit()	