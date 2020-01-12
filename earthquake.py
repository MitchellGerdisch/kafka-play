'''
Description:
Provides a simple class and method to get earthquake data.
The first time it's called, it'll return data from the previous X hours.
Then each time it's called, it'll wait and get data for the next X minutes.
'''

import requests
import time


class Earthquake:
	# initalize start time to be now in format used by API

	def __init__(self, interval):
		self.interval = interval # time in minutes to wait for each subsequent set of data
		self.end_epoch_time = int(time.time()) # End time is now for the first time through
		self.start_epoch_time = self.end_epoch_time - (self.interval * 3600) # for the first time through, get data from the previous "interval" hours

	def get_quake_set(self):

		# Get now time
		now_epoch_time = int(time.time())
		# If now is earlier than the end time, wait until it is end time
		if (now_epoch_time < self.end_epoch_time):
			sleep(self.end_epoch_time - now_epoch_time)		

		# And reset end time to now so we are synched up for this invocation.
		# If we did the sleep above, this is pretty much a no-op.
		# If we didn't have to sleep, then we are resetting the end time to catch up with the time we are at now
		self.end_epoch_time = now_epoch_time			

		# Call the API to get data between the start and end time
		start_time =  time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime(self.start_epoch_time))
		end_time =  time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime(self.end_epoch_time))
		base_api_endpoint = "https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson"
		response = requests.get(base_api_endpoint+"&starttime="+start_time+"&endtime="+end_time)

		# Update the the start and end time for the next invocation.
		self.start_epoch_time = self.end_epoch_time # Next time start where we just ended.
		self.end_epoch_time = self.start_epoch_time + (self.interval * 60) # and end "interval" minutes in the future

		return response.json()




