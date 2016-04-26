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

class AngularValueType:
	"""
	This class combines a numeric value with an angular measurement unit.

	Proper construction should call constructor with either radians=x or degrees=y; not both.  The constructor will calculate the complementary.  The value of the angle can then be retrieve from the .degrees or .radians value as needed.

	Another class member, called .valued is available to determine if the class members contain meaningful values.

	If the constructor is called without either argument, the .valued variable is False, and the numeric variables are None.

	If the constructor is called with both arguments, they will be assigned if they agree to within a small tolerance, or a ValueError is thrown.
	"""
	def __init__(self, radians=None, degrees=None):
		"""
		Constructor for the class.  Call it with either radians or degrees, not both.

		>>> a = AngularValueType(radians=math.pi)
		>>> a = AngularValueType(degrees=180)
		"""

		if not radians and not degrees:
			self.valued = False
			self.radians = None
			self.degrees = None
		elif radians and not degrees:
			self.valued = True
			self.radians = radians
			self.degrees = math.degrees(radians)
		elif degrees and not radians:
			self.valued = True
			self.radians = math.radians(degrees)
			self.degrees = degrees
		else: # degrees and radians
			if abs(math.degrees(radians) - degrees) > 0.01:
				raise ValueError("Radians and Degrees both given but don't agree")
			self.valued = True
			self.radians = radians
			self.degrees = degrees

def dayOfYear(datetimeInstance):
	"""
	Calculates the day of year (1-366) given a Python datetime.datetime instance.  Basically a wrapper around the native tm\_yday parameter to ensure it is a full datetime instance in subsequent calculations. If the type is *not* datetime.datetime, this will throw a TypeError

	:param datetimeInstance: [Python native datetime.datetime] The current date and time to be used in this calculation of day of year.
	:returns: [Integer] [dimensionless] The day of year, from 1 to 365 for non-leap years and 1-366 for leap years.

	"""
	if not type(datetimeInstance) is datetime:
		raise TypeError("Expected datetime.datetime type")
	dayOfYear = datetimeInstance.timetuple().tm_yday

	return dayOfYear

def equationOfTime(datetimeInstance):
	"""
	Calculates the Equation of Time for a given date.  I wasn't able to get the McQuiston equation to match the values in the given table.  I ended up using a different formulation here: http://holbert.faculty.asu.edu/eee463/SolarCalcs.pdf.

	:param datetimeInstance: [Python native datetime.datetime] The current date and time to be used in this calculation of day of year.
	:returns: [Float] The equation of time, which is the difference between local civil time and local solar time

	"""
	degrees = (dayOfYear(datetimeInstance) - 81.0) * (360.0/365.0)
	radians = math.radians(degrees)
	equationOfTimeMinutes = 9.87 * math.sin(2*radians) - 7.53 * math.cos(radians) - 1.5 * math.sin(radians)
	return equationOfTimeMinutes

def declinationAngle(datetimeInstance):
	"""
	Calculates the Solar Declination Angle for a given date. The solar declination angle is the angle between a line connecting the center of the sun and earth and the project of that line on the equatorial plane. Calculation is based on McQuiston.

	:param datetimeInstance: [Python native datetime.datetime] The current date and time to be used in this calculation of day of year.
	:returns: [AngularValueType] The solar declination angle in an AngularValueType with both radian and degree versions

	"""
	radians = math.radians((dayOfYear(datetimeInstance) - 1.0) * (360.0/365.0))
	decAngleDeg = 0.3963723 - 22.9132745 * math.cos(radians) + 4.0254304 * math.sin(radians) - 0.387205 * math.cos(2.0 * radians) + 0.05196728 * math.sin(2.0 * radians) - 0.1545267 * math.cos(3.0 * radians) + 0.08479777 * math.sin(3.0 * radians)
	return AngularValueType(degrees=decAngleDeg)

def localCivilTime(datetimeInstance, daylightSavingsOn, longitude, standardMeridian):
	"""
	Calculates the local civil time for a given set of time and location conditions.  The local civil time is the local time based on prime meridian and longitude

	:param datetimeInstance: [Python native datetime.datetime] The current date and time to be used in this calculation of day of year.
	:param daylightSavingsOn: [Boolean] A flag if the current time is a daylight savings number.  If True, the hour is decremented.
	:param longitude: [Float] [degrees west] The current longitude in degrees west of the prime meridian.  For Golden, CO, the variable should be = 105.2.
	:param standardMeridian: [Float] [degrees west] The local standard meridian for the location, in degrees west of the prime meridian.  For Golden, CO, the variable should be = 105.

	:returns: [Float] [hours] Returns the local civil time in hours for the given date/time/location

	"""
	if daylightSavingsOn:
		civilHour = datetimeInstance.time().hour - 1
	else:
		civilHour = datetimeInstance.time().hour
	localCivilTimeHours = civilHour + datetimeInstance.time().minute/60.0 + datetimeInstance.time().second/3600.0 - 4*(longitude - standardMeridian)/60.0
	return localCivilTimeHours

def localSolarTime(datetimeInstance, daylightSavingsOn, longitude, standardMeridian):
	"""
	Calculates the local solar time for a given set of time and location conditions. The local solar time is the local civil time that has been corrected by the equation of time.

	:param datetimeInstance: [Python native datetime.datetime] The current date and time to be used in this calculation of day of year.
	:param daylightSavingsOn: [Boolean] A flag if the current time is a daylight savings number.  If True, the hour is decremented.
	:param longitude: [Float] [degrees west] The current longitude in degrees west of the prime meridian.  For Golden, CO, the variable should be = 105.2.
	:param standardMeridian: [Float] [degrees west] The local standard meridian for the location, in degrees west of the prime meridian.  For Golden, CO, the variable should be = 105.

	:returns: [Float] [hours] Returns the local solar time in hours for the given date/time/location

	"""

	localSolarTimeHours = localCivilTime(datetimeInstance, daylightSavingsOn, longitude, standardMeridian) + equationOfTime(datetimeInstance)/60.0
	return localSolarTimeHours

def hourAngle(datetimeInstance, daylightSavingsOn, longitude, standardMeridian):
	"""
	Calculates the current hour angle for a given set of time and location conditions. The hour angle is the angle between solar noon and the current solar angle, so at local solar noon the value is zero, in the morning it is below zero, and in the afternoon it is positive.

	:param datetimeInstance: [Python native datetime.datetime] The current date and time to be used in this calculation of day of year.
	:param daylightSavingsOn: [Boolean] A flag if the current time is a daylight savings number.  If True, the hour is decremented.
	:param longitude: [Float] [degrees west] The current longitude in degrees west of the prime meridian.  For Golden, CO, the variable should be = 105.2.
	:param standardMeridian: [Float] [degrees west] The local standard meridian for the location, in degrees west of the prime meridian.  For Golden, CO, the variable should be = 105.

	:returns: [AngularValueType] The hour angle in an AngularValueType with both radian and degree versions

	"""
	localSolarTimeHours = localSolarTime(datetimeInstance, daylightSavingsOn, longitude, standardMeridian)
	hourAngleDeg = 15.0 * (localSolarTimeHours - 12)
	return AngularValueType(degrees=hourAngleDeg)

def altitudeAngle(datetimeInstance, daylightSavingsOn, longitude, standardMeridian, latitude):
	"""
	Calculates the current solar altitude angle for a given set of time and location conditions. The solar altitude angle is the angle between the sun rays and the horizontal plane.

	:param datetimeInstance: [Python native datetime.datetime] The current date and time to be used in this calculation of day of year.
	:param daylightSavingsOn: [Boolean] A flag if the current time is a daylight savings number.  If True, the hour is decremented.
	:param longitude: [Float] [degrees west] The current longitude in degrees west of the prime meridian.  For Golden, CO, the variable should be = 105.2.
	:param standardMeridian: [Float] [degrees west] The local standard meridian for the location, in degrees west of the prime meridian.  For Golden, CO, the variable should be = 105.
	:param latitude: [Float] [degrees north] The local latitude for the location, in degrees north of the equator.  For Golden, CO, the variable should be = 39.75.

	:returns: [AngularValueType] The solar altitude angle in an AngularValueType with both radian and degree versions

	"""
	declinRadians = declinationAngle(datetimeInstance).radians
	hourRadians = hourAngle(datetimeInstance, daylightSavingsOn, longitude, standardMeridian).radians
	latitudeRad = math.radians(latitude)
	altitudeAngleRadians = math.asin( math.cos(latitudeRad) * math.cos(declinRadians) * math.cos(hourRadians) + math.sin(latitudeRad) * math.sin(declinRadians) )
	return AngularValueType(radians=altitudeAngleRadians)

def solarAzimuthAngle(datetimeInstance, daylightSavingsOn, longitude, standardMeridian, latitude):
	"""
	Calculates the current solar azimuth angle for a given set of time and location conditions. The solar azimuth angle is the angle in the horizontal plane between due north and the sun.  It is measured clockwise, so that east is +90 degrees and west is +270 degrees.

	:param datetimeInstance: [Python native datetime.datetime] The current date and time to be used in this calculation of day of year.
	:param daylightSavingsOn: [Boolean] A flag if the current time is a daylight savings number.  If True, the hour is decremented.
	:param longitude: [Float] [degrees west] The current longitude in degrees west of the prime meridian.  For Golden, CO, the variable should be = 105.2.
	:param standardMeridian: [Float] [degrees west] The local standard meridian for the location, in degrees west of the prime meridian.  For Golden, CO, the variable should be = 105.
	:param latitude: [Float] [degrees north] The local latitude for the location, in degrees north of the equator.  For Golden, CO, the variable should be = 39.75.

	:returns: [AngularValueType] The solar azimuth angle in an AngularValueType with both radian and degree versions.  NOTE: If the sun is down, the Float values in the dictionary are None.

	"""
	declinRadians = declinationAngle(datetimeInstance).radians
	altitudeDegrees = altitudeAngle(datetimeInstance, daylightSavingsOn, longitude, standardMeridian, latitude).degrees
	altitudeRadians = math.radians(altitudeDegrees)
	if altitudeDegrees < 0: # sun is down
		return AngularValueType()
	zenithRadians = math.radians(90-altitudeDegrees)
	latitudeRad = math.radians(latitude)
	hourRad = hourAngle(datetimeInstance, daylightSavingsOn, longitude, standardMeridian).radians
	arccosineFromSouth = math.acos( ( math.sin(altitudeRadians) * math.sin(latitudeRad) - math.sin(declinRadians) ) / ( math.cos(altitudeRadians) * math.cos(latitudeRad)) )
	if hourRad < 0:
		azimuthFromSouth = arccosineFromSouth
	else:
		azimuthFromSouth = -arccosineFromSouth
	azimuthAngleRadians = math.radians(180)-azimuthFromSouth
	return AngularValueType(radians=azimuthAngleRadians)

def wallAzimuthAngle(datetimeInstance, daylightSavingsOn, longitude, standardMeridian, latitude, surfaceAzimuthDeg):
	"""
	Calculates the current wall azimuth angle for a given set of time and location conditions, and a surface orientation. The wall azimiuth angle is the angle in the horizontal plane between the solar azimuth and the vertical wall's outward facing normal vector.

	:param datetimeInstance: [Python native datetime.datetime] The current date and time to be used in this calculation of day of year.
	:param daylightSavingsOn: [Boolean] A flag if the current time is a daylight savings number.  If True, the hour is decremented.
	:param longitude: [Float] [degrees west] The current longitude in degrees west of the prime meridian.  For Golden, CO, the variable should be = 105.2.
	:param standardMeridian: [Float] [degrees west] The local standard meridian for the location, in degrees west of the prime meridian.  For Golden, CO, the variable should be = 105.
	:param latitude: [Float] [degrees north] The local latitude for the location, in degrees north of the equator.  For Golden, CO, the variable should be = 39.75.
	:param surfaceAzimuthDeg: [Float] [degrees CW from North] The angle between north and the outward facing normal vector of the wall, measured as positive clockwise from south (southwest facing surface: 225, northwest facing surface: 315)

	:returns: [AngularValueType] The wall azimuth angle in an AngularValueType with both radian and degree versions.  NOTE: If the sun is behind the surface, the Float values in the dictionary are None.

	"""
	thisSurfaceAzimuthDeg = surfaceAzimuthDeg % 360
	operator = 0
	solarAzimuth = solarAzimuthAngle(datetimeInstance, daylightSavingsOn, longitude, standardMeridian, latitude).degrees
	if solarAzimuth is None: # sun is down
		return AngularValueType()
	wallAzimuthDegrees = solarAzimuth - thisSurfaceAzimuthDeg
	if wallAzimuthDegrees > 90 or wallAzimuthDegrees < -90:
		return AngularValueType()
	return AngularValueType(degrees=wallAzimuthDegrees)

def solarAngleOfIncidence(datetimeInstance, daylightSavingsOn, longitude, standardMeridian, latitude, surfaceAzimuthDeg):
	"""
	Calculates the solar angle of incidence for a given set of time and location conditions, and a surface orientation. The solar angle of incidence is the angle between the solar ray vector incident on the surface, and the outward facing surface normal vector.

	:param datetimeInstance: [Python native datetime.datetime] The current date and time to be used in this calculation of day of year.
	:param daylightSavingsOn: [Boolean] A flag if the current time is a daylight savings number.  If True, the hour is decremented.
	:param longitude: [Float] [degrees west] The current longitude in degrees west of the prime meridian.  For Golden, CO, the variable should be = 105.2.
	:param standardMeridian: [Float] [degrees west] The local standard meridian for the location, in degrees west of the prime meridian.  For Golden, CO, the variable should be = 105.
	:param latitude: [Float] [degrees north] The local latitude for the location, in degrees north of the equator.  For Golden, CO, the variable should be = 39.75.
	:param surfaceAzimuthDeg: [Float] [degrees CW from North] The angle between north and the outward facing normal vector of the wall, measured as positive clockwise from south (southwest facing surface: 225, northwest facing surface: 315)

	:returns: [AngularValueType] The solar angle of incidence in an AngularValueType with both radian and degree versions.  NOTE: If the sun is down, or behind the surface, the Float values in the dictionary are None.

	"""
	wallAzimuthRad = wallAzimuthAngle(datetimeInstance, daylightSavingsOn, longitude, standardMeridian, latitude, surfaceAzimuthDeg).radians
	if wallAzimuthRad is None:
		return AngularValueType()
	altitudeRad = altitudeAngle(datetimeInstance, daylightSavingsOn, longitude, standardMeridian, latitude).radians
	incidenceAngleRadians = math.acos( math.cos(altitudeRad) * math.cos(wallAzimuthRad) )
	#print("inside solarAngleOfIncidence:, datetime = %s, wallAzimuth = %s, altitude = %s, incidence = %s" % (datetimeInstance, wallAzimuthRad, altitudeRad, incidenceAngleRadians))
	return AngularValueType(radians=incidenceAngleRadians)

def directRadiationOnSurface(datetimeInstance, daylightSavingsOn, longitude, standardMeridian, latitude, surfaceAzimuthDeg, horizontalDirectIrradiation):
	"""
	Calculates the amount of direct solar radiation incident on a surface for a given set of time and location conditions, a surface orientation, and a total global horizontal direct irradiation. This is merely the global horizontal direct solar irradiation time the angle of incidence on the surface.

	:param datetimeInstance: [Python native datetime.datetime] The current date and time to be used in this calculation of day of year.
	:param daylightSavingsOn: [Boolean] A flag if the current time is a daylight savings number.  If True, the hour is decremented.
	:param longitude: [Float] [degrees west] The current longitude in degrees west of the prime meridian.  For Golden, CO, the variable should be = 105.2.
	:param standardMeridian: [Float] [degrees west] The local standard meridian for the location, in degrees west of the prime meridian.  For Golden, CO, the variable should be = 105.
	:param latitude: [Float] [degrees north] The local latitude for the location, in degrees north of the equator.  For Golden, CO, the variable should be = 39.75.
	:param surfaceAzimuthDeg: [Float] [degrees CW from North] The angle between north and the outward facing normal vector of the wall, measured as positive clockwise from south (southwest facing surface: 225, northwest facing surface: 315)
	:param horizontalDirectIrradiation: [Float] [any] The global horizontal direct irradiation at the location.

	:returns: [Dictionary {DR, Float}] The incident direct radiation on the surface.  The units of this return value match the units of the parameter :horizontalDirectIrradiation:

	"""
	theta = solarAngleOfIncidence(datetimeInstance, daylightSavingsOn, longitude, standardMeridian, latitude, surfaceAzimuthDeg).radians
	if theta is None:
		return None
	return horizontalDirectIrradiation * math.cos( theta )

def getDirectDiffuseSplit(datetimeInstance, daylightSavingsOn, longitude, standardMeridian, latitude, horizontalTotalIrradiation):
	"""
	Calculates the direct and diffuse split for a given amount of global total horizontal irradiation

	:param datetimeInstance: [Python native datetime.datetime] The current date and time to be used in this calculation of day of year.
        :param daylightSavingsOn: [Boolean] A flag if the current time is a daylight savings number.  If True, the hour is decremented.
        :param longitude: [Float] [degrees west] The current longitude in degrees west of the prime meridian.  For Golden, CO, the variable should be = 105.2.
        :param standardMeridian: [Float] [degrees west] The local standard meridian for the location, in degrees west of the prime meridian.  For Golden, CO, the variable should be = 105.
        :param latitude: [Float] [degrees north] The local latitude for the location, in degrees north of the equator.  For Golden, CO, the variable should be = 39.75.
	:param horizontalTotalIrradiation: [Float] The total horizontal irradiation at a given time

	:returns: [Dictionary {String, Float}] A dictionary returning the direct and diffuse portions of a given horizontal irradiation value, two keys: "direct" and "diffuse" are in the dictionary
	"""
	# mostly found from:  Modelling Methods for Energy in Buildings By Chris Underwood, Francis Yik, 2004, Blackwell Publishing, 
	# for a horizontal surface, the theta between surface normal and the vector to the sun is simply the altitude angle
	theta_h = altitudeAngle(datetimeInstance, daylightSavingsOn, longitude, standardMeridian, latitude)
	# some cases we can return early:
	#  if theta is nil or negative, then just assume any solar radiation is diffuse and return no direct portion
	#  if the solar radiation is zero, just leave with zero
	if ( not theta_h.valued ) or ( theta_h.degrees <= 0.0 ):
		return {"diffuse":horizontalTotalIrradiation, "direct":0.0}
	elif horizontalTotalIrradiation <= 0.0:
		return {"diffuse":0.0, "direct":0.0}
	# calculate total extraterrestrial radiation
	# reference: Duffie and Beckman 1991
	I_0 = 1367   # solar constant, W/m2, 
	n_day = dayOfYear(datetimeInstance)     # day of year, 
	I_E = I_0 * ( 1 + 0.033 * math.cos( 360 * n_day / 365 ) ) * math.cos( theta_h.radians )
	# calculate clearness index
	# reference: convention, no specific ref
	k_c = horizontalTotalIrradiation / I_E # clearness index, ratio 0-1
	if k_c > 1.0:
		k_c = 1.0 # should this be OK to have more solar radiation than that allowed on a clear day? -- NO, right?
		horizontalTotalIrradiation = I_E
	# calculate the diffuse/total ratio
	# reference: Skartveit & Olseth 1987
	pi = 3.14159265358979
	# calculate k values: k_1, k_2, and k_max so that we know which region we are in
	k_1 = 0.83 - 0.56 * math.exp( -0.06 * theta_h.degrees )
	k_2 = 0.95 * k_1
	alpha =  ( 1 / math.sin( theta_h.radians ) )**0.6
	k_b_max = 0.81**alpha
	d_1 = 0.07 + 0.046 * (90 - theta_h.degrees) / (theta_h.degrees + 3)
	bigK1 = 0.5 * ( 1 + math.sin( pi * ( k_c - 0.22 ) / ( k_1 - 0.22 ) - pi / 2 ) )
	bigK2 = 0.5 * ( 1 + math.sin( pi * ( k_2 - 0.22 ) / ( k_1 - 0.22 ) - pi / 2 ) )
	d_2 = 1 - ( 1 - d_1 ) * ( 0.11 * math.sqrt( bigK2 ) + 0.15 * bigK2 + 0.74 * bigK2**2 )
	k_max = (k_b_max + d_2*k_2/(1-k_2))/(1 + d_2*k_2/(1-k_2))
	if k_c < 0.22:
		diffuse_ratio = 1
	elif k_c < k_2:
		diffuse_ratio = 1 - ( 1 - d_1 ) * ( 0.11 * math.sqrt( bigK1 ) + 0.15 * bigK1 + 0.74 * bigK1**2 )
	elif k_c < k_max:
		diffuse_ratio = d_2 * k_2 * ( 1 - k_c ) / ( k_c * ( 1 - k_2 ) )	
	else:
		d_max = d_2 * k_2 * ( 1 - k_max ) / ( k_max * ( 1 - k_2 ) )
		diffuse_ratio = 1 - k_max * ( 1 - d_max ) / k_c
	return {"diffuse": horizontalTotalIrradiation * diffuse_ratio, "direct": horizontalTotalIrradiation * ( 1 - diffuse_ratio )}
