'''
Prep for testing kafka producer-consumer based pipeline.

WARNING WARNING WARNING: It will destroy the earthquakes2 table in the postgres DB that the consumer is set up to write to.
Maybe there's a to-do here around creating a test-only connector and a test DB in postgres. 
But for now this scorched-earth policy will be fine.
'''
import psycopg2
import os

print("")
print("********************************************************************")
print("PREPARING EARTHQUAKE CONSUMER BASED PIPELINE TEST")
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
pg_cursor.execute("DROP TABLE IF EXISTS "+PG_TABLE+";")
pg_connection.commit()

