#!/usr/local/bin/python3

'''
Uses Earthquake Class to get a set of earthquake data which it then puts into a kafka topic.
Each earthquake data item placed into the stream consists of:
- Unique earthquake event identifier
- Magnitude of the quake
- Time of the quake (UTC)
- Latitude of the quake
- Longitude of the quake
'''

from earthquake import Earthquake
from kafka-p

# Connect to kafka and create the topic



# Instantiate an instance of Earthquake
quake = Earthquake(1) 

# loop forever and get earthquake data
while True:
	print("start time: "+str(quake.start_epoch_time)+"; end time: "+str(quake.end_epoch_time))
	quake_data_set = quake.get_quake_set()	
	quake_data = quake_data_set["features"]
	for quake_entry in quake_data:
		quake_kafka_entry = {
			"id": quake_entry["id"],
			"mag": quake_entry["properties"]["mag"],
			"time": quake_entry["properties"]["time"],
			"lat": quake_entry["geometry"]["coordinates"][1],
			"long": quake_entry["geometry"]["coordinates"][0],
			"place": quake_entry["properties"]["place"]
		}	

	# Push the quake entry to the kafka stream
