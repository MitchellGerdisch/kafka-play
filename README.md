# Earthquake Data Pipeline Using Kafka and PostgresDB

This is a small project that uses the [US Geological Service Earthquake API](https://earthquake.usgs.gov/fdsnws/event/1/#methods) to collect earthquake data and then push it into a kafka stream which is then read on the other side by a connector that then pushes the data into a Postgres DB.

## Prerequisites
* Kafka cluster with
	* Topic: earthquakes
* JDBC sink connector 
	* Naturally, it should be connected to the Kafka cluster.
	* See the configuration notes below.
* Postgres DB with
	* DB: defaultdb

## Usage
* Set the following environment variables:
```
export KAFKA_BOOTSTRAP_SERVER="<KAFKA BOOTSTRAP SERVER>:<KAFKA PORT>"
export KAFKA_USER="<KAFKA USER>"
export KAFKA_PASSWORD="<KAFKA USER PASSWORD>"
export KAFKA_CA_FILE="<PATH TO CA FILE FOR KAFKA CLUSTER>"
export KAFKA_CERT_FILE="<PATH TO CERT FILE FOR KAFKA CLUSTER>"
export KAFKA_KEY_FILE="<PATH TO KEY FILE FOR KAFKA CLUSTER>"
```
* Run: earthquake_kafka_producer.py
	* This will start by gathering data for the last several hours and then check for earthquakes every minute thereafter.

## Output
* The earthquakes table in the Postgres DB will show the earthquake data.

## JDBC Sink Connector Configuration Notes
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








