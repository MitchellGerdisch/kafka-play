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
- Description of where the earthquake occurred.

PREREQUISITES:
- Kafka service with a topic named "earthquakes"
- Applicable credentials configured as per the local kafka_creds module.

TO-DOs:
- Add automation to create the topic. 
'''

from earthquake import Earthquake
from kafka import KafkaProducer
from kafka_creds import KafkaCreds
import json
import sys

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
	value_serializer=lambda m: json.dumps(m).encode('utf-8')
)

# Instantiate an instance of Earthquake
quake = Earthquake(20)  # after the initial grab, will wait 30 minutes between requests for new data. Earthquakes don't happen all that frequently - thankfully

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


# Get earthquake data and push it into kafka 
# Loop forever unless we are in Test mode 
keep_running = True
while keep_running:
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
	# See if being run in test mode in which case we just get the initial set of earthquakes from the previous several hours and don't wait for any additional events
	if (len(sys.argv) > 1) and (sys.argv[1] == "TEST"):
		keep_running = False

