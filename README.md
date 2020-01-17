# Earthquake Data Pipeline Using Kafka and PostgresDB

This is a small project that uses the [US Geological Service Earthquake API](https://earthquake.usgs.gov/fdsnws/event/1/#methods) to collect earthquake data and then push it into a kafka stream which is then consuconsumedplaced in a Postgres DB.

## Connector-Based or Consumer-Based
This repo supports two methods of getting the data into the Postgres DB: 
* Using a kafka connector, or 
* Using a python kafka consumer script. 

One or the other can be used. Additionally, the logic supports running both at the same time - they write to two separate Postgres tables.

## Prerequisites
* Kafka cluster with
	* Topic: earthquakes
* (Optional) JDBC sink connector 
	* Naturally, it should be connected to the Kafka cluster.
	* See the configuration notes below.
* Postgres DB with
	* DB: defaultdb

## Environment Set Up Requirements
* Set the following environment variables:
```
export KAFKA_BOOTSTRAP_SERVER="<KAFKA BOOTSTRAP SERVER>:<KAFKA PORT>"
export KAFKA_USER="<KAFKA USER>"
export KAFKA_PASSWORD="<KAFKA USER PASSWORD>"
export KAFKA_CA_FILE="<PATH TO CA FILE FOR KAFKA CLUSTER>"
export KAFKA_CERT_FILE="<PATH TO CERT FILE FOR KAFKA CLUSTER>"
export KAFKA_KEY_FILE="<PATH TO KEY FILE FOR KAFKA CLUSTER>"

export PG_HOST="<POSTGRES DB HOST>"
export PG_PORT="<POSTGRES DB PORT>"
export PG_USER="<POSTGRES DB USER>"
export PG_PASSWORD="<POSTGRES DB USER PASSWORD>"

```
* Store the Kafka CA, Cert and Key files as per the applicable environment variables.

## Usage
* Run: earthquake_kafka_producer.py
	* This will start by gathering data for the last several hours and then check for earthquakes every minute thereafter.
* (Optional) Run: earthquake_kafka_consumer.py 
    * This is only needed it using the consumer instead of or in addition to using the JDBC sink connector.

## Output
### Connector Based Pipeline
* A table named "earthquakes" is created and populated in the Postgres DB.
### Consumer Based Pipeline
* A table named "earthquakes2" is created and populated in the Postgres DB.

## Testing
### Automated Testing Travis-CI
A travis.yml is included to allow Travis-CI testing. You will need to manage the enironment variables and CA, Cert and Key files.
### Manual Testing
Run the producer and, optionally, the consumer and inspect the "earthquakes" table (if using connector) and, if applicable "earthquakes2" tables (if using consumer) in the database.
Additionally, one can leverage the ".*-test_prep" and ".*-test_check" scripts to reset the table and dump the table. See the travis.yml script block to see how these scripts are used to test the system.

# JDBC Sink Connector Configuration Notes
Set the configuration file as follows: 
```
{
    "name": "kafka-pg-connector",
    "connector.class": "io.aiven.connect.jdbc.JdbcSinkConnector",
    "key.converter": "org.apache.kafka.connect.json.JsonConverter",
    "value.converter": "org.apache.kafka.connect.json.JsonConverter",
    "config.action.reload": "none",
    "topics": "earthquakes",
    "connection.url": "jdbc:postgresql://<KAFKA CLUSTER ENDPOINT>:<KAFKA CLUSTER PORT>/defaultdb?sslmode=require",
    "connection.user": "<USER>",
    "connection.password": "<PASSWORD>",
    "auto.create": "true",
    "insert.mode": "upsert",
    "pk.mode": "record_value",
    "pk.fields": "id",
    "value.converter.schemas.enable": "true",
    "key.converter.schemas.enable": "true"
}
```
For details, see: 
[Aiven Kafka JDBC Connector Docs](https://github.com/aiven/aiven-kafka-connect-jdbc/blob/master/docs/sink-connector.md)








