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
	"""
	This class is essentially an Enum container holding enums for degrees and radians to be used as dictionary keys in function return values
	"""
	Degrees = -1
	Radians = -2

def dayOfYear(datetimeInstance):
	"""
	#### Summary

	Calculates the day of year (1-366) given a Python datetime.datetime instance.

	#### Description

	Basically a wrapper around the native tm_yday parameter to ensure it is a full datetime instance in subsequent calculations.
	If the type is _not_ datetime.datetime, this will throw a TypeError

	#### Arguments:

	* datetimeInstance
		- Type: Python native datetime.datetime
		- Description: The current date and time to be used in this calculation of day of year

	#### Returns

	* returnValue
		- Type: Integer
		- Description: The day of year, from 1 to 365 for non-leap years and 1-366 for leap years
		- Units: -

	"""
	if not type(datetimeInstance) is datetime:
		raise TypeError("Expected datetime.datetime type")
	dayOfYear = datetimeInstance.timetuple().tm_yday

	return dayOfYear

def equationOfTime(datetimeInstance):
	"""

	#### Summary

	Calculates the Equation of Time for a given date

	#### Description

	I wasn't able to get the McQuiston equation to match the values in the given table
	I ended up using a different formulation here: http://holbert.faculty.asu.edu/eee463/SolarCalcs.pdf

	#### Arguments:

	* datetimeInstance
		- Type: Python native datetime.datetime
		- Description: The current date and time to be used in this calculation of day of year

	#### Returns

	* returnValue
		- Type: Float
		- Description: The equation of time, which is the difference between local civil time and local solar time
		- Units: minutes

	"""
	degrees = (dayOfYear(datetimeInstance) - 81.0) * (360.0/365.0)
	radians = math.radians(degrees)
	equationOfTimeMinutes = 9.87 * math.sin(2*radians) - 7.53 * math.cos(radians) - 1.5 * math.sin(radians)
	return equationOfTimeMinutes

def declinationAngle(datetimeInstance):
	"""

	#### Summary

	Calculates the Solar Declination Angle for a given date

	#### Description

	The solar declination angle is the angle between a line connecting the center of the sun and earth and the project of that line on the equatorial plane
	Calculation is based on McQuiston.

	#### Arguments:

	* datetimeInstance
		- Type: Python native datetime.datetime
		- Description: The current date and time to be used in this calculation of day of year

	#### Returns

	* returnValue
		- Type: Dictionary{ DR, Float }
		- Description: The solar declination angle in a dictionary providing both radian and degree versions
		- Units: { DR.Degrees: degrees, DR.Radians: radians }

	"""
	radians = math.radians((dayOfYear(datetimeInstance) - 1.0) * (360.0/365.0))
	decAngleDeg = 0.3963723 - 22.9132745 * math.cos(radians) + 4.0254304 * math.sin(radians) - 0.387205 * math.cos(2.0 * radians) + 0.05196728 * math.sin(2.0 * radians) - 0.1545267 * math.cos(3.0 * radians) + 0.08479777 * math.sin(3.0 * radians)
	decAngleRad = math.radians(decAngleDeg)
	return {DR.Degrees: decAngleDeg, DR.Radians: decAngleRad}

def localCivilTime(datetimeInstance, daylightSavingsOn, longitude, standardMeridian):
	"""

	#### Summary

	Calculates the local civil time for a given set of time and location conditions

	#### Description

	The local civil time is the local time based on prime meridian and longitude

	#### Arguments:

	* datetimeInstance
		- Type: Python native datetime.datetime
		- Description: The current date and time to be used in this calculation of day of year
	* daylightSavingsOn
		- Type: Boolean
		- Description: A flag if the current time is a daylight savings number.  If True, the hour is decremented.
	* longitude
		- Type: Float
		- Description: The current longitude in degrees west of the prime meridian.  For Golden, CO, the variable should be = 105.2.
		- Units: degrees west
	* standardMeridian
		- Type: Float
		- Description: The local standard meridian for the location, in degrees west of the prime meridian.  For Golden, CO, the variable should be = 105.
		- Units: degrees west

	#### Returns

	* returnValue
		- Type: Float
		- Description: Returns the local civil time in hours for the given date/time/location
		- Units: hours

	"""
	if daylightSavingsOn:
		civilHour = datetimeInstance.time().hour - 1
	else:
		civilHour = datetimeInstance.time().hour
	localCivilTimeHours = civilHour + datetimeInstance.time().minute/60.0 + datetimeInstance.time().second/3600.0 - 4*(longitude - standardMeridian)/60.0
	return localCivilTimeHours

def localSolarTime(datetimeInstance, daylightSavingsOn, longitude, standardMeridian):
	"""

	#### Summary

	Calculates the local solar time for a given set of time and location conditions

	#### Description

	The local solar time is the local civil time that has been corrected by the equation of time

	#### Arguments:

	* datetimeInstance
		- Type: Python native datetime.datetime
		- Description: The current date and time to be used in this calculation of day of year
	* daylightSavingsOn
		- Type: Boolean
		- Description: A flag if the current time is a daylight savings number.  If True, the hour is decremented.
	* longitude
		- Type: Float
		- Description: The current longitude in degrees west of the prime meridian.  For Golden, CO, the variable should be = 105.2.
		- Units: degrees west
	* standardMeridian
		- Type: Float
		- Description: The local standard meridian for the location, in degrees west of the prime meridian.  For Golden, CO, the variable should be = 105.
		- Units: degrees west

	#### Returns

	* returnValue
		- Type: Float
		- Description: Returns the local solar time in hours for the given date/time/location
		- Units: hours

	"""

	localSolarTimeHours = localCivilTime(datetimeInstance, daylightSavingsOn, longitude, standardMeridian) + equationOfTime(datetimeInstance)/60.0
	return localSolarTimeHours

def hourAngle(datetimeInstance, daylightSavingsOn, longitude, standardMeridian):
	"""

	#### Summary

	Calculates the current hour angle for a given set of time and location conditions

	#### Description

	The hour angle is the angle between solar noon and the current solar angle, so at local solar noon the value is zero, and at sunrise/sunset, the value maximizes.

	#### Arguments:

	* datetimeInstance
		- Type: Python native datetime.datetime
		- Description: The current date and time to be used in this calculation of day of year
	* daylightSavingsOn
		- Type: Boolean
		- Description: A flag if the current time is a daylight savings number.  If True, the hour is decremented.
	* longitude
		- Type: Float
		- Description: The current longitude in degrees west of the prime meridian.  For Golden, CO, the variable should be = 105.2.
		- Units: degrees west
	* standardMeridian
		- Type: Float
		- Description: The local standard meridian for the location, in degrees west of the prime meridian.  For Golden, CO, the variable should be = 105.
		- Units: degrees west

	#### Returns

	* returnValue
		- Type: Dictionary{ DR, Float }
		- Description: The hour angle in a dictionary providing both radian and degree versions
		- Units: { DR.Degrees: degrees, DR.Radians: radians }

	"""
	localSolarTimeHours = localSolarTime(datetimeInstance, daylightSavingsOn, longitude, standardMeridian)
	hourAngleDeg = abs(15.0 * (localSolarTimeHours - 12))
	hourAngleRad = math.radians(hourAngleDeg)
	return {DR.Degrees: hourAngleDeg, DR.Radians: hourAngleRad}

def altitudeAngle(datetimeInstance, daylightSavingsOn, longitude, standardMeridian, latitude):
	"""

	#### Summary

	Calculates the current solar altitude angle for a given set of time and location conditions

	#### Description

	The solar altitude angle is the angle between the sun rays and the horizontal plane

	#### Arguments:

	* datetimeInstance
		- Type: Python native datetime.datetime
		- Description: The current date and time to be used in this calculation of day of year
	* daylightSavingsOn
		- Type: Boolean
		- Description: A flag if the current time is a daylight savings number.  If True, the hour is decremented.
	* longitude
		- Type: Float
		- Description: The current longitude in degrees west of the prime meridian.  For Golden, CO, the variable should be = 105.2.
		- Units: degrees west
	* standardMeridian
		- Type: Float
		- Description: The local standard meridian for the location, in degrees west of the prime meridian.  For Golden, CO, the variable should be = 105.
		- Units: degrees west
	* latitude
		- Type: Float
		- Description: The local latitude for the location, in degrees north of the equator.  For Golden, CO, the variable should be = 39.75.
		- Units: degrees north

	#### Returns

	* returnValue
		- Type: Dictionary{ DR, Float }
		- Description: The solar altitude angle in a dictionary providing both radian and degree versions
		- Units: { DR.Degrees: degrees, DR.Radians: radians }

	"""
	declinRadians = declinationAngle(datetimeInstance)[DR.Radians]
	hourRadians = hourAngle(datetimeInstance, daylightSavingsOn, longitude, standardMeridian)[DR.Radians]
	latitudeRad = math.radians(latitude)
	altitudeAngleRadians = math.asin( math.cos(latitudeRad) * math.cos(declinRadians) * math.cos(hourRadians) + math.sin(latitudeRad) * math.sin(declinRadians) )
	altitudeAngleDegrees = math.degrees(altitudeAngleRadians)
	return {DR.Degrees: altitudeAngleDegrees, DR.Radians: altitudeAngleRadians}

def solarAzimuthAngle(datetimeInstance, daylightSavingsOn, longitude, standardMeridian, latitude):
	"""

	#### Summary

	Calculates the current solar azimuth angle for a given set of time and location conditions

	#### Description

	The solar azimuth angle is the angle in the horizontal plane between due south and the sun

	#### Arguments:

	* datetimeInstance
		- Type: Python native datetime.datetime
		- Description: The current date and time to be used in this calculation of day of year
	* daylightSavingsOn
		- Type: Boolean
		- Description: A flag if the current time is a daylight savings number.  If True, the hour is decremented.
	* longitude
		- Type: Float
		- Description: The current longitude in degrees west of the prime meridian.  For Golden, CO, the variable should be = 105.2.
		- Units: degrees west
	* standardMeridian
		- Type: Float
		- Description: The local standard meridian for the location, in degrees west of the prime meridian.  For Golden, CO, the variable should be = 105.
		- Units: degrees west
	* latitude
		- Type: Float
		- Description: The local latitude for the location, in degrees north of the equator.  For Golden, CO, the variable should be = 39.75.
		- Units: degrees north

	#### Returns

	* returnValue
		- Type: Dictionary{ DR, Float }
		- Description: The solar azimuth angle in a dictionary providing both radian and degree versions
		- Units: { DR.Degrees: degrees, DR.Radians: radians }

	"""
	declinRadians = declinationAngle(datetimeInstance)[DR.Radians]
	altitudeRadians = altitudeAngle(datetimeInstance, daylightSavingsOn, longitude, standardMeridian, latitude)[DR.Radians]
	latitudeRad = math.radians(latitude)
	azimuthAngleRadians = math.acos( ( math.sin(altitudeRadians) * math.sin(latitudeRad) - math.sin(declinRadians) ) / ( math.cos(altitudeRadians) * math.cos(latitudeRad)) )
	azimuthAngleDegrees = math.degrees(azimuthAngleRadians)
	return {DR.Degrees: azimuthAngleDegrees, DR.Radians: azimuthAngleRadians}

def wallAzimuthAngle(datetimeInstance, daylightSavingsOn, longitude, standardMeridian, latitude, surfaceAzimuthDeg):
	"""

	#### Summary

	Calculates the current wall azimuth angle for a given set of time and location conditions, and a surface orientation

	#### Description

	The wall azimiuth angle is the angle in the horizontal plane between the solar azimuth and the vertical wall's outward facing normal vector

	#### Arguments:

	* datetimeInstance
		- Type: Python native datetime.datetime
		- Description: The current date and time to be used in this calculation of day of year
	* daylightSavingsOn
		- Type: Boolean
		- Description: A flag if the current time is a daylight savings number.  If True, the hour is decremented.
	* longitude
		- Type: Float
		- Description: The current longitude in degrees west of the prime meridian.  For Golden, CO, the variable should be = 105.2.
		- Units: degrees west
	* standardMeridian
		- Type: Float
		- Description: The local standard meridian for the location, in degrees west of the prime meridian.  For Golden, CO, the variable should be = 105.
		- Units: degrees west
	* latitude
		- Type: Float
		- Description: The local latitude for the location, in degrees north of the equator.  For Golden, CO, the variable should be = 39.75.
		- Units: degrees north
	* surfaceAzimuthDeg
		- Type: Float
		- Description: The angle between south and the outward facing normal vector of the wall, measured as positive clockwise from south (southwest facing surface: 45, northwest facing surface: 135)
		- Units: degrees clockwise from south

	#### Returns

	* returnValue
		- Type: Dictionary{ DR, Float }
		- Description: The wall azimuth angle in a dictionary providing both radian and degree versions
		- Units: { DR.Degrees: degrees, DR.Radians: radians }

	"""
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
	"""

	#### Summary

	Calculates the solar angle of incidence for a given set of time and location conditions, and a surface orientation

	#### Description

	The solar angle of incidence is the angle between the solar ray vector incident on the surface, and the outward facing surface normal vector

	#### Arguments:

	* datetimeInstance
		- Type: Python native datetime.datetime
		- Description: The current date and time to be used in this calculation of day of year
	* daylightSavingsOn
		- Type: Boolean
		- Description: A flag if the current time is a daylight savings number.  If True, the hour is decremented.
	* longitude
		- Type: Float
		- Description: The current longitude in degrees west of the prime meridian.  For Golden, CO, the variable should be = 105.2.
		- Units: degrees west
	* standardMeridian
		- Type: Float
		- Description: The local standard meridian for the location, in degrees west of the prime meridian.  For Golden, CO, the variable should be = 105.
		- Units: degrees west
	* latitude
		- Type: Float
		- Description: The local latitude for the location, in degrees north of the equator.  For Golden, CO, the variable should be = 39.75.
		- Units: degrees north
	* surfaceAzimuthDeg
		- Type: Float
		- Description: The angle between south and the outward facing normal vector of the wall, measured as positive clockwise from south (southwest facing surface: 45, northwest facing surface: 135)
		- Units: degrees clockwise from south

	#### Returns

	* returnValue
		- Type: Dictionary{ DR, Float }
		- Description: The solar angle of incidence in a dictionary providing both radian and degree versions
		- Units: { DR.Degrees: degrees, DR.Radians: radians }

	"""
	solarAzimuthRadiansAbsolute = abs(wallAzimuthAngle(datetimeInstance, daylightSavingsOn, longitude, standardMeridian, latitude, surfaceAzimuthDeg)[DR.Radians])
	azimuthAngleRadians = math.acos( math.cos(altitudeAngle(datetimeInstance, daylightSavingsOn, longitude, standardMeridian, latitude)[DR.Radians]) * math.cos(solarAzimuthRadiansAbsolute) )
	azimuthAngleDegrees = math.degrees(azimuthAngleRadians)
	return {DR.Degrees: azimuthAngleDegrees, DR.Radians: azimuthAngleRadians}

def directRadiationOnSurface(datetimeInstance, daylightSavingsOn, longitude, standardMeridian, latitude, surfaceAzimuthDeg, horizontalDirectIrradiation):
	"""

	#### Summary

	Calculates the amount of direct solar radiation incident on a surface for a given set of time and location conditions, a surface orientation, and a total global horizontal direct irradiation

	#### Description

	This is merely the global horizontal direct solar irradiation time the angle of incidence on the surface

	#### Arguments:

	* datetimeInstance
		- Type: Python native datetime.datetime
		- Description: The current date and time to be used in this calculation of day of year
	* daylightSavingsOn
		- Type: Boolean
		- Description: A flag if the current time is a daylight savings number.  If True, the hour is decremented.
	* longitude
		- Type: Float
		- Description: The current longitude in degrees west of the prime meridian.  For Golden, CO, the variable should be = 105.2.
		- Units: degrees west
	* standardMeridian
		- Type: Float
		- Description: The local standard meridian for the location, in degrees west of the prime meridian.  For Golden, CO, the variable should be = 105.
		- Units: degrees west
	* latitude
		- Type: Float
		- Description: The local latitude for the location, in degrees north of the equator.  For Golden, CO, the variable should be = 39.75.
		- Units: degrees north
	* surfaceAzimuthDeg
		- Type: Float
		- Description: The angle between south and the outward facing normal vector of the wall, measured as positive clockwise from south (southwest facing surface: 45, northwest facing surface: 135)
		- Units: degrees clockwise from south
	* horizontalDirectIrradiation
		- Type: Float
		- Description: The global horizontal direct irradiation at the location
		- Units: any, return value will match the input units

	#### Returns

	* returnValue
		- Type: Float
		- Description: The incident direct radiation on the surface
		- Units: output matches units of the input argument: horizontalDirectIrradiation

	"""
	return horizontalDirectIrradiation * math.cos( solarAngleOfIncidence(datetimeInstance, daylightSavingsOn, longitude, standardMeridian, latitude, surfaceAzimuthDeg)[DR.Radians] )
