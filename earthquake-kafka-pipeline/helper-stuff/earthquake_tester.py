#!/usr/local/bin/python3
'''
Quick hacks to test earthquake module
'''

import time
from earthquake_batch import Earthquake

quake = Earthquake(0.25)

print(quake.hours)
print(quake.start_epoch_time)
print(quake.end_epoch_time)
print("XXXXX")

quake_data = quake.get_quake_set()
print(quake_data)
