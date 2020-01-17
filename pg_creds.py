'''
DESCRIPTION:
This class is used to instantiate a set of credentials for accesing a Postgres DB.
Currently uses environment variables to store credentials.

PREREQUISITES:
Set up the following environment variables:
- PG_HOST => <POSTGRES DB CLUSTER DNS NAME OR IP ADDRESS>
- PG_PORT => <POSTGRES DB PORT>
- PG_USER => Postgres DB username
- PG_PASSWORD => Postgrees DB password
'''

import os
class PostgresCreds:
	def __init__(self):
		self.pg_host = os.getenv('PG_HOST')	
		self.pg_port = os.getenv('PG_PORT')
		self.pg_user = os.getenv('PG_USER')
		self.pg_password = os.getenv('PG_PASSWORD')


