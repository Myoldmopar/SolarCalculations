#!/usr/bin/env python

# add the solar directory to the path so we can import it
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'solar'))

# import the datetime library so we construct proper datetime instances
from datetime import datetime

# import the solar library
import solar

# import the csv library for easier output
import csv

# Golden, CO
longitude = 104.85
stdmeridian = 105
latitude = 39.57

with open('/tmp/compare_winter_angles_library.csv', 'w') as csvfile:
	mywriter = csv.writer(csvfile)
	mywriter.writerow(['Hour', 'Hour Angle', 'Solar Altitude', 'Solar Azimuth'])
	for hour in range(0,24): # gives zero-based hours as expected in the datetime constructor
		x = hour
		dt = datetime(2001, 12, 21, hour, 00, 00)
		thour = solar.hourAngle(dt, False, longitude, stdmeridian)[solar.DR.Degrees]
		altitude = solar.altitudeAngle(dt, False, longitude, stdmeridian, latitude)[solar.DR.Degrees]
		azimuth = solar.solarAzimuthAngle(dt, False, longitude, stdmeridian, latitude)[solar.DR.Degrees]
		mywriter.writerow([x, -thour, altitude, azimuth])

with open('/tmp/compare_summer_angles_library.csv', 'w') as csvfile:
	mywriter = csv.writer(csvfile)
	mywriter.writerow(['Hour', 'Hour Angle', 'Solar Altitude', 'Solar Azimuth'])
	for hour in range(0,24): # gives zero-based hours as expected in the datetime constructor
		x = hour
		dt = datetime(2001, 7, 21, hour, 00, 00)
		thour = solar.hourAngle(dt, False, longitude, stdmeridian)[solar.DR.Degrees]
		altitude = solar.altitudeAngle(dt, False, longitude, stdmeridian, latitude)[solar.DR.Degrees]
		azimuth = solar.solarAzimuthAngle(dt, False, longitude, stdmeridian, latitude)[solar.DR.Degrees]
		mywriter.writerow([x, -thour, altitude, azimuth])

with open('/tmp/compare_summer_incidence_library.csv', 'w') as csvfile:
	mywriter = csv.writer(csvfile)
	mywriter.writerow(['Hour', 'East Incidence', 'West Incidence'])
	for hour in range(0,24): # gives zero-based hours as expected in the datetime constructor
		x = hour
		dt = datetime(2001, 7, 21, hour, 30, 00)
		theta_west = solar.solarAngleOfIncidence(dt, False, longitude, stdmeridian, latitude, 270)[solar.DR.Degrees]
		theta_east = solar.solarAngleOfIncidence(dt, False, longitude, stdmeridian, latitude, 90)[solar.DR.Degrees]
		mywriter.writerow([x, theta_east, theta_west])
