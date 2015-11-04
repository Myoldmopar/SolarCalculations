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

# calculate hour, azimuth, and altitude angle for a winter day in Golden, CO
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


## calculate wall azimuth angles for a summer day in Golden, CO
#longitude = 105.2
#stdmeridian = 105
#latitude = 39.75
#x = []
#east_wall_normal_from_north = 90
#east_az = []
#south_wall_normal_from_north = 180
#south_az = []
#west_wall_normal_from_north = 270
#west_az = []
#for hour in range(0,24): # gives zero-based hours as expected in the datetime constructor
	#x.append(hour)
	#dt = datetime(2001, 6, 21, hour, 00, 00)
	#east_az.append(solar.wallAzimuthAngle(dt, True, longitude, stdmeridian, latitude, east_wall_normal_from_north)[solar.DR.Degrees])
	#south_az.append(solar.wallAzimuthAngle(dt, True, longitude, stdmeridian, latitude, south_wall_normal_from_north)[solar.DR.Degrees])
	#west_az.append(solar.wallAzimuthAngle(dt, True, longitude, stdmeridian, latitude, west_wall_normal_from_north)[solar.DR.Degrees])

#plt.plot(x, east_az,  'r', label='East Wall Azimuth Angle')
#plt.plot(x, south_az, 'g', label='South Wall Azimuth Angle')
#plt.plot(x, west_az,  'b', label='West Wall Azimuth Angle')
#plt.xlim([0,23])
#plt.ylim([-90,180])
#plt.suptitle("Wall Azimuth Angles", fontsize=14, fontweight='bold')
#plt.xlabel("Hour of Day -- Clock Time")
#plt.ylabel("Angle [degrees]")
#plt.grid(True, axis='both')
#plt.legend()
#plt.savefig(os.path.join(os.path.dirname(__file__), '..', '..', 'SolarCalculations.wiki/DemoSolarAnglesWallAzimuths.png'))

#### reset
#plt.close()

## calculate solar angle of incidence for a summer day in Golden, CO
#longitude = 105.2
#stdmeridian = 105
#latitude = 39.75
#x = []
#east_wall_normal_from_north = 90
#east_theta = []
#east_az = []
#alt = []
#for hour in range(0,24): # gives zero-based hours as expected in the datetime constructor
	#x.append(hour)
	#dt = datetime(2001, 6, 21, hour, 00, 00)
	#east_az.append(solar.wallAzimuthAngle(dt, True, longitude, stdmeridian, latitude, east_wall_normal_from_north)[solar.DR.Degrees])
	#east_theta.append(solar.solarAngleOfIncidence(dt, True, longitude, stdmeridian, latitude, east_wall_normal_from_north)[solar.DR.Degrees])
	#alt.append(solar.altitudeAngle(dt, True, longitude, stdmeridian, latitude)[solar.DR.Degrees])

#plt.plot(x, alt,        'r', label='Solar Altitude Angle')
#plt.plot(x, east_az,    'g', label='East Wall Azimuth Angle')
#plt.plot(x, east_theta, 'b', label='East Wall Incidence Angle')
#plt.xlim([0,23])
#plt.ylim([-90,180])
#plt.suptitle("Wall Solar Incidence Angles", fontsize=14, fontweight='bold')
#plt.xlabel("Hour of Day -- Clock Time")
#plt.ylabel("Angle [degrees]")
#plt.grid(True, axis='both')
#plt.legend()
#plt.savefig(os.path.join(os.path.dirname(__file__), '..', '..', 'SolarCalculations.wiki/DemoSolarAnglesSolarIncidence.png'))
