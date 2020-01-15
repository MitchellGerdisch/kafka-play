# Earthquake Data Pipeline Using Kafka and PostgresDB

This is a small project that uses a US Geological Service earthquake API to collect earthquake data and then push it into a kafka stream which is then read on the other side by a connector that then pushes the data into a Postgres DB.

## Prerequisites
* Kafka cluster