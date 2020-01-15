'''
This module provides a class and method for getting earthquake data for given interval of time.
The caller needs to specify the interval for quake data when instantiating the object.
This interval will then be used each time the get_next_quake_set() method is called to wait that long before asking the USGS for 
earthquake data that spans what is basically the timeframe since the last call.
'''
import requests
import time


class Earthquake:
	# initalize start time to be now in format used by API

	def __init__(self, interval):
		self.interval = interval
		self.start_epoch_time = int(time.time())



	def get_next_quake_set(self):
		# sleep for the specified interval.
		time.sleep(self.interval)
		# get the "now" time
		end_epoch_time = int(time.time())
		# format the start time and end time time for use with the API
		start_time =  time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime(self.start_epoch_time))
		end_time =  time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime(end_epoch_time))
		# update the start time with the new end time so that next time we'll start where we left off.
		self.start_epoch_time = end_epoch_time

		# Call the API to get eartquake information
		base_api_endpoint = "https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson"
		response = requests.get(base_api_endpoint+"&starttime="+start_time+"&endtime="+end_time)
		return response.json()




