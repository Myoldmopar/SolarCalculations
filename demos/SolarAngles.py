#!/usr/bin/env python

# add the solar directory to the path so we can import it
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'solar'))

# import the datetime library so we construct proper datetime instances
from datetime import datetime

# import the solar library
import solar

# import the plotting library for demonstration -- pip install matplotlib should suffice
import matplotlib.pyplot as plt
import numpy

# calculate times in Stillwater, OK -- to demonstrate the effect of longitude not lining up with the stdmeridian
longitude = 97.05
stdmeridian = 90
latitude = 36.11
x = []
lct = []
lst = []
for hour in range(0,24): # gives zero-based hours as expected in the datetime constructor
	x.append(hour)
	dt = datetime(2001, 6, 21, hour, 00, 00)
	lct.append(solar.localCivilTime(dt, True, longitude, stdmeridian))
	lst.append(solar.localSolarTime(dt, True, longitude, stdmeridian))

plt.plot(x,      'black',  label='Clock Time')
plt.plot(x, lct, 'grey',   label='Civil Time', linewidth=6)
plt.plot(x, lst, 'yellow', label='Solar Time')
plt.xlim([0,23])
plt.suptitle("Time Values for Stillwater, OK on June 21", fontsize=14, fontweight='bold')
plt.xlabel("Hour of Day -- Clock Time")
plt.ylabel("Time [hours]")
plt.grid(True, axis='both')
plt.legend()
plt.savefig(os.path.join(os.path.dirname(__file__), '..', '..', 'SolarCalculations.wiki/DemoSolarAnglesCivilSolarTime.png'))

#### reset
plt.close()

# calculate hour angle for a summer day in Golden, CO
longitude = 105.2
stdmeridian = 105
latitude = 39.75
x = []
hours = []
for hour in range(0,24): # gives zero-based hours as expected in the datetime constructor
	x.append(hour)
	dt = datetime(2001, 6, 21, hour, 00, 00)
	hours.append(solar.hourAngle(dt, True, longitude, stdmeridian).degrees)

plt.plot(x, hours, 'b', label='Hour Angle')
plt.xlim([0,23])
plt.suptitle("Hour Angle", fontsize=14, fontweight='bold')
plt.xlabel("Hour of Day -- Clock Time")
plt.ylabel("Angle [degrees]")
plt.grid(True, axis='both')
plt.legend()
plt.savefig(os.path.join(os.path.dirname(__file__), '..', '..', 'SolarCalculations.wiki/DemoSolarAnglesHour.png'))

#### reset
plt.close()

# calculate solar altitude angles for Winter and Summer days in Golden, CO
longitude = 105.2
stdmeridian = 105
latitude = 39.75
x = []
beta_winter = []
beta_summer = []
for hour in range(0,24): # gives zero-based hours as expected in the datetime constructor
	x.append(hour)
	dt = datetime(2001, 12, 21, hour, 00, 00)
	beta_winter.append(solar.altitudeAngle(dt, False, longitude, stdmeridian, latitude).degrees)
	dt = datetime(2001, 6, 21, hour, 00, 00)
	beta_summer.append(solar.altitudeAngle(dt, True, longitude, stdmeridian, latitude).degrees)

plt.plot(x, beta_winter, 'b', label='Winter')
plt.plot(x, beta_summer, 'r', label='Summer')
plt.xlim([0,23])
plt.suptitle("Solar Altitude Angle", fontsize=14, fontweight='bold')
plt.xlabel("Hour of Day -- Clock Time")
plt.ylabel("Angle [degrees]")
plt.grid(True, axis='both')
plt.legend()
plt.savefig(os.path.join(os.path.dirname(__file__), '..', '..', 'SolarCalculations.wiki/DemoSolarAngles1.png'))

#### reset
plt.close()

# calculate solar azimuth angle for a summer day in Golden, CO
longitude = 105.2
stdmeridian = 105
latitude = 39.75
x = []
solar_az = []
for hour in range(0,24): # gives zero-based hours as expected in the datetime constructor
	x.append(hour)
	dt = datetime(2001, 6, 21, hour, 00, 00)
	solar_az.append(solar.solarAzimuthAngle(dt, True, longitude, stdmeridian, latitude).degrees)

plt.plot(x, solar_az, 'b', label='Solar Azimuth Angle')
plt.xlim([0,23])
plt.suptitle("Solar Azimuth Angle", fontsize=14, fontweight='bold')
plt.xlabel("Hour of Day -- Clock Time")
plt.ylabel("Angle [degrees]")
plt.grid(True, axis='both')
plt.legend()
plt.savefig(os.path.join(os.path.dirname(__file__), '..', '..', 'SolarCalculations.wiki/DemoSolarAnglesSolarAzimuth.png'))

### reset
plt.close()

# calculate wall azimuth angles for a summer day in Golden, CO
longitude = 105.2
stdmeridian = 105
latitude = 39.75
x = []
east_wall_normal_from_north = 90
east_az = []
south_wall_normal_from_north = 180
south_az = []
west_wall_normal_from_north = 270
west_az = []
for hour in range(0,24): # gives zero-based hours as expected in the datetime constructor
	x.append(hour)
	dt = datetime(2001, 6, 21, hour, 00, 00)
	east_az.append(solar.wallAzimuthAngle(dt, True, longitude, stdmeridian, latitude, east_wall_normal_from_north).degrees)
	south_az.append(solar.wallAzimuthAngle(dt, True, longitude, stdmeridian, latitude, south_wall_normal_from_north).degrees)
	west_az.append(solar.wallAzimuthAngle(dt, True, longitude, stdmeridian, latitude, west_wall_normal_from_north).degrees)

plt.plot(x, east_az,  'r', label='East Wall Azimuth Angle')
plt.plot(x, south_az, 'g', label='South Wall Azimuth Angle')
plt.plot(x, west_az,  'b', label='West Wall Azimuth Angle')
plt.xlim([0,23])
plt.ylim([-90,180])
plt.suptitle("Wall Azimuth Angles", fontsize=14, fontweight='bold')
plt.xlabel("Hour of Day -- Clock Time")
plt.ylabel("Angle [degrees]")
plt.grid(True, axis='both')
plt.legend()
plt.savefig(os.path.join(os.path.dirname(__file__), '..', '..', 'SolarCalculations.wiki/DemoSolarAnglesWallAzimuths.png'))

### reset
plt.close()

# calculate solar angle of incidence for a summer day in Golden, CO
longitude = 105.2
stdmeridian = 105
latitude = 39.75
x = []
east_wall_normal_from_north = 90
east_theta = []
east_az = []
alt = []
for hour in range(0,24): # gives zero-based hours as expected in the datetime constructor
	x.append(hour)
	dt = datetime(2001, 6, 21, hour, 00, 00)
	east_az.append(solar.wallAzimuthAngle(dt, True, longitude, stdmeridian, latitude, east_wall_normal_from_north).degrees)
	east_theta.append(solar.solarAngleOfIncidence(dt, True, longitude, stdmeridian, latitude, east_wall_normal_from_north).degrees)
	alt.append(solar.altitudeAngle(dt, True, longitude, stdmeridian, latitude).degrees)

plt.plot(x, alt,        'r', label='Solar Altitude Angle')
plt.plot(x, east_az,    'g', label='East Wall Azimuth Angle')
plt.plot(x, east_theta, 'b', label='East Wall Incidence Angle')
plt.xlim([0,23])
plt.ylim([-90,180])
plt.suptitle("Wall Solar Incidence Angles", fontsize=14, fontweight='bold')
plt.xlabel("Hour of Day -- Clock Time")
plt.ylabel("Angle [degrees]")
plt.grid(True, axis='both')
plt.legend()
plt.savefig(os.path.join(os.path.dirname(__file__), '..', '..', 'SolarCalculations.wiki/DemoSolarAnglesSolarIncidence.png'))
