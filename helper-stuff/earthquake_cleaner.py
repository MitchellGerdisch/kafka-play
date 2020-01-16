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
BOOTSTRAP_SERVER = creds.bootstrap_server
USER = creds.user
PASSWORD = creds.password
CA_FILE = creds.ca_file
CERT_FILE = creds.cert_file
KEY_FILE = creds.key_file



# This script receives messages from a Kafka topic


consumer = KafkaConsumer(
    "earthquakes",
    auto_offset_reset="earliest",
    client_id="quake-client",
    group_id="quake-group",
    security_protocol="SSL",
    bootstrap_servers=BOOTSTRAP_SERVER,
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