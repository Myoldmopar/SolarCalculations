# This file exhaustively tests the entirety of lib/solar.py

import sys
import os

# add the source directory to the path so the unit test framework can find it
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'solar'))

import unittest
from datetime import datetime
from solar import *

class TestDayOfYear(unittest.TestCase):

	def test_firstDayOfYear(self):
		self.assertEqual(dayOfYear(datetime(1999,01,01,00,00,00)), 001)
		self.assertEqual(dayOfYear(datetime(2000,01,01,00,00,00)), 001)

	def test_lastDayOfYear(self):
		self.assertEqual(dayOfYear(datetime(1995,12,31,00,00,00)), 365) # regular year
		self.assertEqual(dayOfYear(datetime(1996,12,31,00,00,00)), 366) # leap year
		self.assertEqual(dayOfYear(datetime(1900,12,31,00,00,00)), 365) # no leap year on centuries!
		self.assertEqual(dayOfYear(datetime(2000,12,31,00,00,00)), 366) # yes leap year on milleniums though!

	def test_badInput(self):
		with self.assertRaises(TypeError):
			dayOfYear(datetime.date(2006,05,20)) # can't just pass in a date
		with self.assertRaises(TypeError):
			dayOfYear(datetime.time(12,00,00)) # can't just pass in a time

	def test_RightNow(self):
		# we don't wrap this in an assertEqual because we don't know what the output will be
		# if it throws, that's a problem and the unittest framework will catch it
		dayOfYear(datetime.now())

class TestEquationOfTime(unittest.TestCase):

	# validation from Table 6-1 of the reference listed above
	def test_EOTon21s(self):
		tolerance = 0.5 # 30 seconds...
		self.assertAlmostEqual(equationOfTime(datetime(2001, 1,21,00,00,00)), -11.2, delta=tolerance)
		self.assertAlmostEqual(equationOfTime(datetime(2001, 2,21,00,00,00)), -13.9, delta=tolerance)
		self.assertAlmostEqual(equationOfTime(datetime(2001, 3,21,00,00,00)),  -7.5, delta=tolerance)
		self.assertAlmostEqual(equationOfTime(datetime(2001, 4,21,00,00,00)),   1.1, delta=tolerance)
		self.assertAlmostEqual(equationOfTime(datetime(2001, 5,21,00,00,00)),   3.3, delta=tolerance)
		self.assertAlmostEqual(equationOfTime(datetime(2001, 6,21,00,00,00)),  -1.4, delta=tolerance)
		self.assertAlmostEqual(equationOfTime(datetime(2001, 7,21,00,00,00)),  -6.2, delta=tolerance)
		self.assertAlmostEqual(equationOfTime(datetime(2001, 8,21,00,00,00)),  -2.4, delta=tolerance)
		self.assertAlmostEqual(equationOfTime(datetime(2001, 9,21,00,00,00)),   7.5, delta=tolerance)
		self.assertAlmostEqual(equationOfTime(datetime(2001,10,21,00,00,00)),  15.4, delta=tolerance)
		self.assertAlmostEqual(equationOfTime(datetime(2001,11,21,00,00,00)),  13.8, delta=tolerance)
		self.assertAlmostEqual(equationOfTime(datetime(2001,12,21,00,00,00)),   1.6, delta=tolerance)

class TestDeclinationAngle(unittest.TestCase):

	# validation from Table 6-1 of the reference listed above
	def test_declinationsOn21s(self):
		tolerance = 1.25 # 1.25 degrees...
		self.assertAlmostEqual(declinationAngle(datetime(2001, 1,21,00,00,00)).degrees, -20.2, delta=tolerance)
		self.assertAlmostEqual(declinationAngle(datetime(2001, 2,21,00,00,00)).degrees, -10.8, delta=tolerance)
		self.assertAlmostEqual(declinationAngle(datetime(2001, 3,21,00,00,00)).degrees,   0.0, delta=tolerance)
		self.assertAlmostEqual(declinationAngle(datetime(2001, 4,21,00,00,00)).degrees,  11.6, delta=tolerance)
		self.assertAlmostEqual(declinationAngle(datetime(2001, 5,21,00,00,00)).degrees,  20.0, delta=tolerance)
		self.assertAlmostEqual(declinationAngle(datetime(2001, 6,21,00,00,00)).degrees,  23.5, delta=tolerance)
		self.assertAlmostEqual(declinationAngle(datetime(2001, 7,21,00,00,00)).degrees,  20.6, delta=tolerance)
		self.assertAlmostEqual(declinationAngle(datetime(2001, 8,21,00,00,00)).degrees,  12.3, delta=tolerance)
		self.assertAlmostEqual(declinationAngle(datetime(2001, 9,21,00,00,00)).degrees,   0.0, delta=tolerance)
		self.assertAlmostEqual(declinationAngle(datetime(2001,10,21,00,00,00)).degrees, -10.5, delta=tolerance)
		self.assertAlmostEqual(declinationAngle(datetime(2001,11,21,00,00,00)).degrees, -19.8, delta=tolerance)
		self.assertAlmostEqual(declinationAngle(datetime(2001,12,21,00,00,00)).degrees, -23.5, delta=tolerance)

class TestLocalCivilTime(unittest.TestCase):

	# validation from example 6-1 of the 5th Edition of McQuiston
	def test_example561(self):
		dt = datetime(2001, 2, 21, 11, 00, 00)
		dst_on = True
		longitude = 95
		stdmeridican = 90
		self.assertAlmostEqual(localCivilTime(dt, dst_on, longitude, stdmeridican), 9.67, delta=0.01)

class TestLocalSolarTime(unittest.TestCase):

	# validation from example 6-1 of the 5th Edition of McQuiston
	def test_example561(self):
		dt = datetime(2001, 2, 21, 11, 00, 00)
		dst_on = True
		longitude = 95
		stdmeridican = 90
		self.assertAlmostEqual(localSolarTime(dt, dst_on, longitude, stdmeridican), 9.43, delta=0.01)

class TestHourAngle(unittest.TestCase):

	# validation from example 6-2 of the 5th Edition of McQuiston
	def test_example562(self):
		dt = datetime(2001, 7, 21, 10, 00, 00)
		dst_on = True
		longitude = 85
		stdmeridican = 90
		self.assertAlmostEqual(localCivilTime(dt, dst_on, longitude, stdmeridican), 9.3, delta=0.1)
		self.assertAlmostEqual(equationOfTime(dt), -6.2, delta=0.2)
		self.assertAlmostEqual(localSolarTime(dt, dst_on, longitude, stdmeridican), 9.23, delta=0.01)
		self.assertAlmostEqual(hourAngle(dt, dst_on, longitude, stdmeridican).degrees, -41.5, delta=0.1) # we are using negative in the morning; positive in the afternoon

	# test solar noon on standard meridian, should be zero right?
	def test_solarNoon(self):
		dt = datetime(2001, 6, 15, 12, 00, 00)  # chose June 15 because EOT goes to near zero on that date
		dst_on = False
		longitude = 90
		stdmeridican = 90
		self.assertAlmostEqual(hourAngle(dt, dst_on, longitude, stdmeridican).degrees, 0, delta=0.1)

class TestAltitudeAngle(unittest.TestCase):

	# validation from example 6-2 of the 5th Edition of McQuiston
	def test_example562(self):
		dt = datetime(2001, 7, 21, 10, 00, 00)
		dst_on = True
		longitude = 85
		stdmeridican = 90
		latitude = 40
		self.assertAlmostEqual(altitudeAngle(dt, dst_on, longitude, stdmeridican, latitude).degrees, 49.7, delta=0.1)

class TestAzimuthAngle(unittest.TestCase):

	# validation from example 6-2 of the 5th Edition of McQuiston
	def test_example562(self):
		dt = datetime(2001, 7, 21, 10, 00, 00)
		dst_on = True
		longitude = 85
		stdmeridican = 90
		latitude = 40
		expectedAzimuthFromSouth = 73.7
		expectedAzimuthFromNorth = 180 - expectedAzimuthFromSouth
		self.assertAlmostEqual(solarAzimuthAngle(dt, dst_on, longitude, stdmeridican, latitude).degrees, expectedAzimuthFromNorth, delta=0.1)

class TestWallAzimuthAngle(unittest.TestCase):

	# test east facing wall where the solar azimuth is known from a prior unit test
	def test_gammaSouthFacing(self):
		dt = datetime(2001, 7, 21, 10, 00, 00)
		dst_on = True
		longitude = 85
		stdmeridican = 90
		latitude = 40
		wallnormal = 90 # north, degrees
		expected_solar_azimuth = 180-73.7
		expected_wall_azimuth = expected_solar_azimuth - wallnormal
		self.assertAlmostEqual(wallAzimuthAngle(dt, dst_on, longitude, stdmeridican, latitude, wallnormal).degrees, expected_wall_azimuth, delta=0.1)

class TestSolarAngleOfIncidence(unittest.TestCase):

	# test east facing surface where solar azimuth and altitude are known from prior unit tests
	def test_thetaSouthFacing(self):
		dt = datetime(2001, 7, 21, 10, 00, 00)
		dst_on = True
		longitude = 85
		stdmeridican = 90
		latitude = 40
		wallnormal = 90 # south, degrees
		expected_solar_azimuth = 180-73.7
		expected_wall_azimuth = math.radians(expected_solar_azimuth - wallnormal)
		expected_solar_altitude = math.radians(49.7)
		expected_theta = math.acos(math.cos(expected_wall_azimuth) * math.cos(expected_solar_altitude))
		self.assertAlmostEqual(solarAngleOfIncidence(dt, dst_on, longitude, stdmeridican, latitude, wallnormal).radians, expected_theta, delta=0.001)

	# test case for azimuth specified greater than 360
	def test_overRatedSurface(self):
		dt = datetime(2001, 7, 21, 10, 00, 00)
		dst_on = True
		longitude = 85
		stdmeridican = 90
		latitude = 40
		wallnormal = 90 # south, degrees
		base_theta = solarAngleOfIncidence(dt, dst_on, longitude, stdmeridican, latitude, wallnormal).radians
		wallnormal = 90+360 # south, degrees
		over_rotated_theta = solarAngleOfIncidence(dt, dst_on, longitude, stdmeridican, latitude, wallnormal).radians
		self.assertAlmostEqual(over_rotated_theta, base_theta, delta=0.001)

class TestRadiationOnSurface(unittest.TestCase):

	def test_directRadiationOnSurfaceSouthFacing(self):
		dt = datetime(2001, 7, 21, 10, 00, 00)
		dst_on = True
		longitude = 85
		stdmeridican = 90
		latitude = 40
		wallnormal = 180 # south, degrees
		theta = solarAngleOfIncidence(dt, dst_on, longitude, stdmeridican, latitude, wallnormal).radians
		insolation = 293 # watts
		self.assertAlmostEqual(directRadiationOnSurface(dt, dst_on, longitude, stdmeridican, latitude, wallnormal, insolation), insolation * math.cos(theta), delta=0.1)

class TestDirectDiffuseSplit(unittest.TestCase):

	def test_directDiffuseSplit(self):
                dt = datetime(2001, 7, 21, 10, 00, 00)
                dst_on = True
                longitude = 85
                stdmeridian = 90
                latitude = 40
                insolation = 800 # watts
		self.assertAlmostEqual(getDirectDiffuseSplit(dt, dst_on, longitude, stdmeridian, latitude, insolation)["diffuse"], 121.484, delta=0.01)
	        
		# now check for a non-zero-solar, yet sundown condition
		dt = datetime(2001, 7, 21, 02, 00, 00)
		self.assertAlmostEqual(getDirectDiffuseSplit(dt, dst_on, longitude, stdmeridian, latitude, insolation)["diffuse"], 800, delta=0.01)

		# now check for a zero solar condition
		dt = datetime(2001, 7, 21, 10, 00, 00)
		insolation = 0.0
		self.assertAlmostEqual(getDirectDiffuseSplit(dt, dst_on, longitude, stdmeridian, latitude, insolation)["diffuse"], 0, delta=0.01)

# allow execution directly as python tests/test_solar.py
if __name__ == '__main__':
	unittest.main()
