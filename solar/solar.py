#!/usr/bin/python

from datetime import datetime
import time
import math

# The calculations here are based on Chapter 6 of 
#'   McQuiston, F.C. and J.D. Parker.  1998.
#'   Heating, Ventilating, and Air Conditioning Analysis and Design, Third Edition.
#'   John Wiley and Sons, New York.

# This was originally a class called SolarPosition, but that was actually a poor design
# The location is capable of moving each call, as well as the date/time.
# So there wasn't anything that needed to persist, and the arguments got real funny between instantiation and function calls
# Thus it is just a little library of functions

class DR:
	Degrees = -1
	Radians = -2

def dayOfYear(datetimeInstance):
	"""
	Returns an integer day of year (1-366) given a Python datetime.datetime instance.
	Basically a wrapper around the native tm_yday parameter to ensure it is a full datetime instance in subsequent calculations
	"""
	# date objects do not have timetuple(), so they will throw here
	# time objects do have that, so they would be valid at runtime, but not what we want
	# we could call a special secret method to ensure we have the right type, but let's just explicitly check type
	if not type(datetimeInstance) is datetime:
		raise TypeError("Expected datetime.datetime type")
	dayOfYear = datetimeInstance.timetuple().tm_yday
	
	#SolarCalcs.output("Day of year = %s" % dayOfYear)
	return dayOfYear

def equationOfTime(datetimeInstance):
	"""
	Returns the Equation of Time for a given date
	I wasn't able to get the McQuiston equation to match the values in the given table
	I ended up using a different formulation here: http://holbert.faculty.asu.edu/eee463/SolarCalcs.pdf
	"""
	degrees = (dayOfYear(datetimeInstance) - 81.0) * (360.0/365.0)
	radians = math.radians(degrees)
	equationOfTimeMinutes = 9.87 * math.sin(2*radians) - 7.53 * math.cos(radians) - 1.5 * math.sin(radians)
	#equationOfTimeMinutes = 229.2 * (0.000075 + 0.001868 * math.cos(radians) - 0.032077 * math.sin(radians) - 0.014615 * math.cos(2 * radians) - 0.04089 * math.sin(2 * radians))
	#self.output("Equation of Time = %i minutes %i seconds" % (int(equationOfTimeMinutes), int((equationOfTimeMinutes-int(equationOfTimeMinutes))*60.0)))
	return equationOfTimeMinutes

def declinationAngle(datetimeInstance):
	"""
	Returns a dictionary of {DR : Float} of the current solar declination angle for a given datetime
	Based on the McQuiston reference
	"""
	radians = math.radians((dayOfYear(datetimeInstance) - 1.0) * (360.0/365.0))
	decAngleDeg = 0.3963723 - 22.9132745 * math.cos(radians) + 4.0254304 * math.sin(radians) - 0.387205 * math.cos(2.0 * radians) + 0.05196728 * math.sin(2.0 * radians) - 0.1545267 * math.cos(3.0 * radians) + 0.08479777 * math.sin(3.0 * radians)
	decAngleRad = math.radians(decAngleDeg)
	#self.output("Declination angle = %s degrees (%s radians)" % (decAngleDeg, decAngleRad))
	return {DR.Degrees: decAngleDeg, DR.Radians: decAngleRad}

def localCivilTime(datetimeInstance, daylightSavingsOn, longitude, standardMeridian):
	"""
	Returns the local civil time in hours for the given datetime instance, a daylight savings time flag, and longitude information in degrees WEST
	"""
	# daylight savings time adjustment
	if daylightSavingsOn:
		civilHour = datetimeInstance.time().hour - 1
	else:
		civilHour = datetimeInstance.time().hour
	localCivilTimeHours = civilHour + datetimeInstance.time().minute/60.0 + datetimeInstance.time().second/3600.0 - 4*(longitude - standardMeridian)/60.0
	#self.output("Local civil time = %s hours" % localCivilTimeHours)
	return localCivilTimeHours

def localSolarTime(datetimeInstance, daylightSavingsOn, longitude, standardMeridian):
	localSolarTimeHours = localCivilTime(datetimeInstance, daylightSavingsOn, longitude, standardMeridian) + equationOfTime(datetimeInstance)/60.0
	#self.output("Local solar time = %s hours" % localSolarTimeHours)
	return localSolarTimeHours

def hourAngle(datetimeInstance, daylightSavingsOn, longitude, standardMeridian):
	localSolarTimeHours = localSolarTime(datetimeInstance, daylightSavingsOn, longitude, standardMeridian)
	hourAngleDeg = abs(15.0 * (localSolarTimeHours - 12))
	hourAngleRad = math.radians(hourAngleDeg)
	#self.output("Hour angle = %s degrees (%s radians)" % (hourAngleDeg, hourAngleRad))
	return {DR.Degrees: hourAngleDeg, DR.Radians: hourAngleRad}

def altitudeAngle(datetimeInstance, daylightSavingsOn, longitude, standardMeridian, latitude):
	declinRadians = declinationAngle(datetimeInstance)[DR.Radians]
	hourRadians = hourAngle(datetimeInstance, daylightSavingsOn, longitude, standardMeridian)[DR.Radians]
	latitudeRad = math.radians(latitude)
	altitudeAngleRadians = math.asin( math.cos(latitudeRad) * math.cos(declinRadians) * math.cos(hourRadians) + math.sin(latitudeRad) * math.sin(declinRadians) )
	altitudeAngleDegrees = math.degrees(altitudeAngleRadians)
	#self.output("Altitude angle = %s degrees (%s radians)" % (altitudeAngleDegrees, altitudeAngleRadians))
	return {DR.Degrees: altitudeAngleDegrees, DR.Radians: altitudeAngleRadians}

def solarAzimuthAngle(datetimeInstance, daylightSavingsOn, longitude, standardMeridian, latitude):
	declinRadians = declinationAngle(datetimeInstance)[DR.Radians]
	altitudeRadians = altitudeAngle(datetimeInstance, daylightSavingsOn, longitude, standardMeridian, latitude)[DR.Radians]
	latitudeRad = math.radians(latitude)
	azimuthAngleRadians = math.acos( ( math.sin(altitudeRadians) * math.sin(latitudeRad) - math.sin(declinRadians) ) / ( math.cos(altitudeRadians) * math.cos(latitudeRad)) )
	azimuthAngleDegrees = math.degrees(azimuthAngleRadians)
	#self.output("Azimuth angle = %s degrees (%s radians)" % (azimuthAngleDegrees, azimuthAngleRadians))
	return {DR.Degrees: azimuthAngleDegrees, DR.Radians: azimuthAngleRadians}

def wallSolarAzimuthAngle(datetimeInstance, daylightSavingsOn, longitude, standardMeridian, latitude, surfaceAzimuthDeg):
	thisSurfaceAzimuthDeg = surfaceAzimuthDeg % 360
	operator = 0
	if localSolarTime(datetimeInstance, daylightSavingsOn, longitude, standardMeridian) < 12:
		if surfaceAzimuthDeg > 180: 
			operator = -1  # morning, east facing walls
		else:
			operator = +1  # morning, west facing walls
	else:
		if surfaceAzimuthDeg > 180: 
			operator = +1  # afternoon, east facing walls
		else:
			operator = -1  # afternoon, west facing walls
	solarAzimuth = solarAzimuthAngle(datetimeInstance, daylightSavingsOn, longitude, standardMeridian, latitude)[DR.Degrees]
	wallAzimuthDegrees = solarAzimuth + operator * surfaceAzimuthDeg
	wallAzimuthRadians = math.radians(wallAzimuthDegrees)
	return {DR.Degrees: wallAzimuthDegrees, DR.Radians: wallAzimuthRadians}

def solarAngleOfIncidence(datetimeInstance, daylightSavingsOn, longitude, standardMeridian, latitude, surfaceAzimuthDeg):
	solarAzimuthRadiansAbsolute = abs(wallSolarAzimuthAngle(datetimeInstance, daylightSavingsOn, longitude, standardMeridian, latitude, surfaceAzimuthDeg)[DR.Radians])
	azimuthAngleRadians = math.acos( math.cos(altitudeAngle(datetimeInstance, daylightSavingsOn, longitude, standardMeridian, latitude)[DR.Radians]) * math.cos(solarAzimuthRadiansAbsolute) )
	azimuthAngleDegrees = math.degrees(azimuthAngleRadians)
	return {DR.Degrees: azimuthAngleDegrees, DR.Radians: azimuthAngleRadians}


# solar position calculation class
class SolarCalcs():
    
	def __init__(self, time, latitude, longitude, standardMeridian, DST_ON, verbose=False):

		# store debug flag
		self.verbose = verbose

		# set the time to use for all calculations
		self.thisTime = time

		# settings
		self.latitudeDeg = latitude #36.7 # degrees north
		self.longitudeDeg = longitude #97.2 # degrees west
		self.standardMeridianDeg = standardMeridian #90.0 # degrees west
		self.DST_ON = DST_ON

		# spew    
		self.output("Using date/time = %s" % self.thisTime)

		# conversions
		self.latitudeRad = math.radians(self.latitudeDeg)
		self.longitudeRad = math.radians(self.longitudeDeg)
		self.standardMeridianRad = math.radians(self.standardMeridianDeg)





	def directRadiationOnSurface(self, surfaceAzimuthAngle, horizontalDirectIrradiation):
		return horizontalDirectIrradiation * math.cos( solarAngleOfIncidence(surfaceAzimuthAngle)[1] )

	def output(self, string):
		if self.verbose:
			print string

# example problem 6-2:
#lat = 40
#lon = -85
#stdmeridian = -90
#DSTFlag = True
#thisTime = time.strptime("2015-07-22 10:00:00", "%Y-%m-%d %H:%M:%S")
#solar = SolarCalcs(thisTime, lat, lon, stdmeridian, DSTFlag)
#print(solar.localCivilTime())
#print(solar.equationOfTime())
#print(solar.localSolarTime())
#print(solar.altitudeAngle()[0])
#print(solar.solarAzimuthAngle()[0])

#surfaceAzimuthAngle = 90 # west facing, measured clockwise from south
#for hour in range(24):
    #thisTime = time.strptime("2015-07-22 %s:00:00" % (hour), "%Y-%m-%d %H:%M:%S")
    #solar = SolarCalcs(thisTime, lat, lon, stdmeridian, DSTFlag)
    #print( "%s,%s,%s,%s" % (solar.altitudeAngle()[0], solar.solarAzimuthAngle()[0], solar.wallSolarAzimuthAngle(surfaceAzimuthAngle)[0], solar.solarAngleOfIncidence(surfaceAzimuthAngle)[0]) )


#print(dayOfYear(datetime(2000,01,01,00,00,00)))
