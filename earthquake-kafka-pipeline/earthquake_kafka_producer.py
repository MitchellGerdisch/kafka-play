#!/usr/local/bin/python3

'''
DESCRIPTION:
Uses Earthquake Class to get a set of earthquake data which it then puts into a kafka topic.
Each earthquake data item placed into the stream consists of:
- Unique earthquake event identifier
- Magnitude of the quake
- Time of the quake (UTC)
- Latitude of the quake
- Longitude of the quake

PREREQUISITES:
- Kafka service with a topic named "earthquakes"
- Applicable credentials configured as per the local kafka_creds kmodule.

TO-DOs:
- Add automation to create the topic. 
'''

from earthquake import Earthquake
from kafka import KafkaProducer
from kafka_creds import KafkaCreds
import json

# Instantiate a set of creds for talking to the Kafka cluster
creds = KafkaCreds()
bootstrap_server = creds.bootstrap_server
user = creds.user
password = creds.password
ca_file = creds.ca_file
cert_file = creds.cert_file
key_file = creds.key_file

# instantiate a kafka producer connection
producer = KafkaProducer(
    bootstrap_servers=bootstrap_server,
    security_protocol="SSL",
    ssl_cafile=ca_file,
    ssl_certfile=cert_file,
    ssl_keyfile=key_file,
	value_serializer=lambda m: json.dumps(m).encode('ascii')
)

# Instantiate an instance of Earthquake
quake = Earthquake(1) 

# As per: https://github.com/aiven/aiven-kafka-connect-jdbc/blob/master/docs/sink-connector.md I need to set up schema info in the JSON
earthquake_db_schema = {
	"type": "struct",
	"fields": [
		{ "field": "id", "type": "string", "optional": False },
		{ "field": "mag", "type": "float", "optional": False },
		{ "field": "time", "type": "int64", "name": "org.apache.kafka.connect.data.Timestamp", "optional": False },
		{ "field": "lat", "type": "float", "optional": False },
		{ "field": "long", "type": "float", "optional": False },
		{ "field": "place", "type": "string", "optional": False }
	]
}


# loop forever and get earthquake data
while True:
	print("Querying earthquake data ...")
	quake_data_set = quake.get_quake_set()	
	quake_data = quake_data_set["features"]
	print ("Found "+str(len(quake_data))+" earthquakes ...")
	for quake_entry in quake_data:
		quake_kafka_entry = {
			"schema": earthquake_db_schema,
			"payload": {
				"id": quake_entry["id"],
				"mag": quake_entry["properties"]["mag"],
				"time": quake_entry["properties"]["time"],
				"lat": quake_entry["geometry"]["coordinates"][1],
				"long": quake_entry["geometry"]["coordinates"][0],
				"place": quake_entry["properties"]["place"]
			}
		}	
		
		# Push the quake entry to the kafka stream
		producer.send("earthquakes", quake_kafka_entry)		

	# Force sending of all messages
	producer.flush()	

