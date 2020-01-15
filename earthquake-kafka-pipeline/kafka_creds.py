'''
DESCRIPTION:
This class is used to instantiate a set of credentials.
Currently uses environment variables to store credentials.

PREREQUISITES:
Set up the following environment variables:
- KAFKA_BOOTSTRAP_SERVER => <KAFKA CLUSTER DNS NAME OR IP ADDRESS>:<KAFKA CLUSTER PORT> 
- KAFKA_USER => Kafka service account username
- KAFKA_PASSWORD => Kafka service account password
- KAFKA_CA_FILE => path to Kafka service CA file
- KAFKA_CERT_FILE => path to Kafka service Certificate file
- KAFKA_KEY_FILE => path to Kafka service Key file
'''

import os
class KafkaCreds:
	def __init__(self):
		self.bootstrap_server = os.getenv('KAFKA_BOOTSTRAP_SERVER')	
		self.user = os.getenv('KAFKA_USER')
		self.password = os.getenv('KAFKA_PASSWORD')
		self.ca_file = os.getenv('KAFKA_CA_FILE')
		self.cert_file = os.getenv('KAFKA_CERT_FILE')	
		self.key_file = os.getenv('KAFKA_KEY_FILE')	
