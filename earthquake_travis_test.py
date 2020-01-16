'''
Used for testing.
NOTE: It will destroy the earthquake DB in the postgres DB that the jdbc sink connector is set up to write to.
Maybe there's a to-do here around creating a test-only connector and a test DB in postgres. 
But for now this scorched-earth policy will be fine.
'''
import psycopg2
import os
import subprocess
import time

# Destroy existing earthquakes DB in Postgres target
PG_HOST = os.getenv("PG_HOST")
PG_PORT = os.getenv("PG_PORT")
PG_USER = os.getenv("PG_USER")
PG_PASSWORD = os.getenv("PG_PASSWORD")

PG_DB = "defaultdb"
PG_TABLE = "earthquakes"

pg_connection = psycopg2.connect("dbname="+PG_DB+" user="+PG_USER+" host="+PG_HOST+" port="+PG_PORT+" password="+PG_PASSWORD)
pg_cursor = pg_connection.cursor()
pg_cursor.execute("DROP TABLE IF EXISTS "+PG_TABLE+";")
pg_connection.commit()

# Now run the producer code
# This will tell how many earthquakes were found.
subprocess.call("$TRAVIS_BUILD_DIR/earthquake_kafka_producer.py TEST", shell=True)

# Sleep a bit to make sure the connector has time to get the data and create the table
time.sleep(10) 

# Now dump the data from the postgres table.
# If the table was not created, then it'll fail and throw an error.
# If the table exists but has no data even and the call above showed it found earthquakes, then we got trouble.
pg_cursor.execute("SELECT * FROM "+PG_TABLE+";")
pg_records = pg_cursor.fetchall()
print(pg_records)
pg_connection.close()
