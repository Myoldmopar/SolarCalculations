#!/usr/bin/env python

# add the solar directory to the path so we can import it
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'solar'))

# import the datetime library so we construct proper datetime instances
from datetime import datetime

# the calendar package has a convenient way to iterate over number of days in a month
from calendar import monthrange

# import the solar library
import solar

# import the csv library for easier output
import csv
import math

# in this validation, we switch the latitude and longitude midway through the year
def getLat(month):
	if month <= 1:
		return 25.0
	else:
		return 45.0
def getLong(month):
	if month <= 1:
		return 95.0
	else:
		return 102.0

stdmeridian = 105
east_wall_normal_from_north = 90
south_wall_normal_from_north = 180
west_wall_normal_from_north = 270
with open('/tmp/eplus_validation_location.csv', 'w') as csvfile:
	mywriter = csv.writer(csvfile)
	mywriter.writerow(['Hour', 'Hour Angle', 'Solar Altitude', 'Solar Azimuth', 'Cos East Wall Theta', 'Cos South Wall Theta', 'Cos West Wall Theta'])
	for month in range(1,3): # just january and february
		thisLat = getLat(month)
		thisLong = getLong(month)
		for day in range(1,monthrange(2011, month)[1]+1): # just make sure it isn't a leap year
			for hour in range(0,24): # gives zero-based hours as expected in the datetime constructor
				x = hour
				dt = datetime(2011, month, day, hour, 30, 00)
				thour = solar.hourAngle(dt, False, thisLong, stdmeridian).degrees
				altitude = solar.altitudeAngle(dt, False, thisLong, stdmeridian, thisLat).degrees
				azimuth = solar.solarAzimuthAngle(dt, False, thisLong, stdmeridian, thisLat).degrees
				east_theta = solar.solarAngleOfIncidence(dt, False, thisLong, stdmeridian, thisLat, east_wall_normal_from_north).radians
				south_theta = solar.solarAngleOfIncidence(dt, False, thisLong, stdmeridian, thisLat, south_wall_normal_from_north).radians
				west_theta = solar.solarAngleOfIncidence(dt, False, thisLong, stdmeridian, thisLat, west_wall_normal_from_north).radians
				if east_theta != None:
					east_theta = math.cos(east_theta)
				if south_theta != None:
					south_theta = math.cos(south_theta)
				if west_theta != None:
					west_theta = math.cos(west_theta)
				mywriter.writerow([x, -thour, altitude, azimuth, east_theta, south_theta, west_theta])

def getWallOrientation(month):
	if month <= 1:
		return 0
	elif month == 2:
		return 90
	elif month == 3:
		return 180
	elif month == 4:
		return 270
	elif month == 5:
		return 360
	else:
		return 0

with open('/tmp/eplus_validation_orientation.csv', 'w') as csvfile:
	mywriter = csv.writer(csvfile)
	mywriter.writerow(['Month', 'Date', 'Hour', 'Hour Angle', 'Solar Altitude', 'Solar Azimuth', 'Cos Wall Theta'])
	for month in range(1,7): # just january through June to get all the way back through 360 and 0 again
		thisLat = 39.57
		thisLong = 104.85
		for day in range(1,monthrange(2011, month)[1]+1): # just make sure it isn't a leap year
			for hour in range(0,24): # gives zero-based hours as expected in the datetime constructor
				x = hour
				for minute in range(0,60): # gives zero-based minutes, I think that's right...it should complain if not
					dt = datetime(2011, month, day, hour, minute, 00)
					thour = solar.hourAngle(dt, False, thisLong, stdmeridian).degrees
					altitude = solar.altitudeAngle(dt, False, thisLong, stdmeridian, thisLat).degrees
					azimuth = solar.solarAzimuthAngle(dt, False, thisLong, stdmeridian, thisLat).degrees
					wall_degrees_from_north = getWallOrientation(month)
					wall_theta = solar.solarAngleOfIncidence(dt, False, thisLong, stdmeridian, thisLat, wall_degrees_from_north).radians
					if wall_theta != None:
						wall_theta = math.cos(wall_theta)
					mywriter.writerow([month, day, x, -thour, altitude, azimuth, wall_theta])


with open('/tmp/quickcheck2.csv', 'w') as csvfile:
	mywriter = csv.writer(csvfile)
	mywriter.writerow(['Month', 'Date', 'Hour', 'Hour Angle', 'Solar Altitude', 'Solar Azimuth', 'Cos Wall Theta'])
	for month in range(1,7): # just january through June to get all the way back through 360 and 0 again
		thisLat = 25
		thisLong = 95
		for day in range(1,monthrange(2011, month)[1]+1): # just make sure it isn't a leap year
			for hour in range(0,24): # gives zero-based hours as expected in the datetime constructor
				x = hour
				for minute in range(0,60): # gives zero-based minutes, I think that's right...it should complain if not
					dt = datetime(2011, month, day, hour, minute, 00)
					thour = solar.hourAngle(dt, False, thisLong, stdmeridian).degrees
					altitude = solar.altitudeAngle(dt, False, thisLong, stdmeridian, thisLat).degrees
					azimuth = solar.solarAzimuthAngle(dt, False, thisLong, stdmeridian, thisLat).degrees
					wall_degrees_from_north = 360
					wall_theta = solar.solarAngleOfIncidence(dt, False, thisLong, stdmeridian, thisLat, wall_degrees_from_north).radians
					if wall_theta != None:
						wall_theta = math.cos(wall_theta)
					mywriter.writerow([month, day, x, -thour, altitude, azimuth, wall_theta])
