'''
Checks if the earthquake consumer-based pipeline completed successfully by seeing if the earthquakes table was created and has content
'''
import psycopg2
import os
import time

print("")
print("********************************************************************")
print("CHECKING EARTHQUAKE CONSUMER BASED PIPELINE DB")
print("You should see a database dump that matches the producer records output seen above as part of the connetor test.")
print("********************************************************************")
print("")

# Destroy existing earthquakes DB in Postgres target
PG_HOST = os.getenv("PG_HOST")
PG_PORT = os.getenv("PG_PORT")
PG_USER = os.getenv("PG_USER")
PG_PASSWORD = os.getenv("PG_PASSWORD")

PG_DB = "defaultdb"
PG_TABLE = "earthquakes2"

pg_connection = psycopg2.connect("dbname="+PG_DB+" user="+PG_USER+" host="+PG_HOST+" port="+PG_PORT+" password="+PG_PASSWORD)
pg_cursor = pg_connection.cursor()

# Sleep a bit to make sure the connector has time to get the data and create the table
time.sleep(15) 

# Now dump the data from the postgres table.
# If the table was not created, then it'll fail and throw an error.
# If the table exists but has no data even and the call above showed it found earthquakes, then we got trouble.
pg_cursor.execute("SELECT * FROM "+PG_TABLE+";")
pg_records = pg_cursor.fetchall()
print(pg_records)
pg_connection.close()
