# Based on this blog: https://help.aiven.io/en/articles/489572-getting-started-with-aiven-kafka


from kafka import KafkaConsumer, KafkaProducer, KafkaAdminClient
import kafka
import ssl
import os
#import logging
#logging.basicConfig(level=logging.DEBUG)



#try:

BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS')	
USER = os.getenv('KAFKA_USER')
PASSWORD = os.getenv('KAFKA_PASSWORD')
CA_FILE = os.getenv('KAFKA_CA_FILE')
CERT_FILE = os.getenv('KAFKA_CERT_FILE')	
KEY_FILE = os.getenv('KAFKA_KEY_FILE')	

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
	}])

exit

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