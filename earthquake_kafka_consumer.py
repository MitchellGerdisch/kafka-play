#!/usr/local/bin/python3

'''
DESCRIPTION:
Pulls data from a Kafka topic that provides earthquake data and stores the information in a Postgres database.
Each earthquake data item pulled from the topic consists of:
- Unique earthquake event identifier
- Magnitude of the quake
- Time of the quake (UTC)
- Latitude of the quake
- Longitude of the quake
- Description of where the earthquake occurred.


PREREQUISITES:
- Kafka service with a topic named "earthquakes"
- Applicable credentials configured as per the local kafka_creds module.

'''

from kafka import KafkaConsumer
from kafka_creds import KafkaCreds
from pg_creds import PostgresCreds
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from datetime import datetime, timezone
import time
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

# Instantiate a set of creds for talking to the Postgres DB
creds = PostgresCreds()
pg_host = creds.pg_host
pg_port = creds.pg_port
pg_user = creds.pg_user
pg_password = creds.pg_password
pg_db = "defaultdb" 
pg_table = "earthquakes2"

# instantiage a postgres client 
pg_connection = psycopg2.connect(dbname=pg_db, user=pg_user, host=pg_host, port=pg_port, password=pg_password)
pg_connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
pg_cursor = pg_connection.cursor()

# create table to which the consumer will push data
table_create_string = "CREATE TABLE IF NOT EXISTS "+pg_table+"(id TEXT PRIMARY KEY, mag REAL, time TIMESTAMP, lat REAL, long REAL, place TEXT);"
pg_cursor.execute(table_create_string)
pg_connection.commit()


# instantiate a kafka producer connection
consumer = KafkaConsumer(
    "earthquakes", 
	auto_offset_reset="earliest",
	client_id="quake-consumer",
	group_id="quake-group",
    bootstrap_servers=bootstrap_server,
    security_protocol="SSL",
    ssl_cafile=ca_file,
    ssl_certfile=cert_file,
    ssl_keyfile=key_file,
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)


for record in consumer:
    payload = record.value["payload"]  # The producer inserts json that can also be consumed by a JDBC sink connector so we need to grab the "payload" bit
    # Get the info for each earthquake
    id = payload["id"]
    mag = str(payload["mag"])
    lat = str(payload["lat"])
    long = str(payload["long"])
    epochtime = payload["time"]/1000.0
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(epochtime))
    place = payload["place"]
    # Insert the data into the DB
    insert_string = "INSERT INTO "+pg_table+"(id, mag, lat, long, time, place) VALUES ('"+id+"',"+mag+","+lat+","+long+",'"+timestamp+"','"+place+"') ON CONFLICT (id) DO UPDATE SET mag="+mag+",lat="+lat+",long="+long+",time='"+timestamp+"',place='"+place+"';"
    pg_cursor.execute(insert_string)
    pg_connection.commit()
    # See if being run in test mode in which case we just get the initial set of earthquakes from the previous several hours and don't wait for any additional events
    if (len(sys.argv) > 1) and (sys.argv[1] == "TEST"):
        print("CONSUMER: Test mode ... exiting")
        break




