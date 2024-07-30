from datetime import date, datetime, time
from math import acos, cos, radians
from unittest import TestCase

from solar_angles.solar import (
    day_of_year,
    equation_of_time,
    declination_angle,
    local_civil_time,
    local_solar_time,
    hour_angle,
    altitude_angle,
    azimuth_angle,
    solar_angle_of_incidence,
    direct_radiation_on_surface,
    wall_azimuth_angle,
    Angular
)


class TestAngularValueType(TestCase):

    def test_construction(self):
        self.assertFalse(Angular().valued)
        self.assertTrue(Angular(degrees=1).valued)
        self.assertTrue(Angular(radians=1).valued)
        self.assertTrue(Angular(degrees=180, radians=3.14159).valued)
        with self.assertRaises(ValueError):
            Angular(degrees=180, radians=2 * 3.14)


class TestDayOfYear(TestCase):

    def test_first_day_of_year(self):
        self.assertEqual(day_of_year(datetime(1999, 1, 1, 00, 00, 00)), 1)
        self.assertEqual(day_of_year(datetime(2000, 1, 1, 00, 00, 00)), 1)

    def test_last_day_of_year(self):
        # regular year
        self.assertEqual(day_of_year(datetime(1995, 12, 31, 00, 00, 00)), 365)
        # leap year
        self.assertEqual(day_of_year(datetime(1996, 12, 31, 00, 00, 00)), 366)
        # no leap year on centuries!
        self.assertEqual(day_of_year(datetime(1900, 12, 31, 00, 00, 00)), 365)
        # yes leap year on millenniums though!
        self.assertEqual(day_of_year(datetime(2000, 12, 31, 00, 00, 00)), 366)

    def test_bad_input(self):
        with self.assertRaises(TypeError):
            # noinspection PyTypeChecker
            day_of_year(date(2006, 5, 20))  # can't just pass in a date
        with self.assertRaises(TypeError):
            # noinspection PyTypeChecker
            day_of_year(time(12, 0, 0))  # can't just pass in a time

    def test_right_now(self):
        # we don't wrap this in an assertEqual because we don't know what the output will be
        # if it throws, that's a problem and the unittest framework will catch it
        day_of_year(datetime.now())


class TestEquationOfTime(TestCase):

    # validation from Table 6-1 of the reference listed above
    def test_equation_of_time_on_the_21s(self):
        tolerance = 0.5  # 30 seconds...
        self.assertAlmostEqual(equation_of_time(datetime(2001, 1, 21, 00, 00, 00)), -11.2, delta=tolerance)
        self.assertAlmostEqual(equation_of_time(datetime(2001, 2, 21, 00, 00, 00)), -13.9, delta=tolerance)
        self.assertAlmostEqual(equation_of_time(datetime(2001, 3, 21, 00, 00, 00)), -7.5, delta=tolerance)
        self.assertAlmostEqual(equation_of_time(datetime(2001, 4, 21, 00, 00, 00)), 1.1, delta=tolerance)
        self.assertAlmostEqual(equation_of_time(datetime(2001, 5, 21, 00, 00, 00)), 3.3, delta=tolerance)
        self.assertAlmostEqual(equation_of_time(datetime(2001, 6, 21, 00, 00, 00)), -1.4, delta=tolerance)
        self.assertAlmostEqual(equation_of_time(datetime(2001, 7, 21, 00, 00, 00)), -6.2, delta=tolerance)
        self.assertAlmostEqual(equation_of_time(datetime(2001, 8, 21, 00, 00, 00)), -2.4, delta=tolerance)
        self.assertAlmostEqual(equation_of_time(datetime(2001, 9, 21, 00, 00, 00)), 7.5, delta=tolerance)
        self.assertAlmostEqual(equation_of_time(datetime(2001, 10, 21, 00, 00, 00)), 15.4, delta=tolerance)
        self.assertAlmostEqual(equation_of_time(datetime(2001, 11, 21, 00, 00, 00)), 13.8, delta=tolerance)
        self.assertAlmostEqual(equation_of_time(datetime(2001, 12, 21, 00, 00, 00)), 1.6, delta=tolerance)


class TestDeclinationAngle(TestCase):

    # validation from Table 6-1 of the reference listed above
    def test_declinations_on_the_21s(self):
        tolerance = 1.25  # 1.25 degrees...
        self.assertAlmostEqual(declination_angle(datetime(2001, 1, 21, 00, 00, 00)).degrees, -20.2, delta=tolerance)
        self.assertAlmostEqual(declination_angle(datetime(2001, 2, 21, 00, 00, 00)).degrees, -10.8, delta=tolerance)
        self.assertAlmostEqual(declination_angle(datetime(2001, 3, 21, 00, 00, 00)).degrees, 0.0, delta=tolerance)
        self.assertAlmostEqual(declination_angle(datetime(2001, 4, 21, 00, 00, 00)).degrees, 11.6, delta=tolerance)
        self.assertAlmostEqual(declination_angle(datetime(2001, 5, 21, 00, 00, 00)).degrees, 20.0, delta=tolerance)
        self.assertAlmostEqual(declination_angle(datetime(2001, 6, 21, 00, 00, 00)).degrees, 23.5, delta=tolerance)
        self.assertAlmostEqual(declination_angle(datetime(2001, 7, 21, 00, 00, 00)).degrees, 20.6, delta=tolerance)
        self.assertAlmostEqual(declination_angle(datetime(2001, 8, 21, 00, 00, 00)).degrees, 12.3, delta=tolerance)
        self.assertAlmostEqual(declination_angle(datetime(2001, 9, 21, 00, 00, 00)).degrees, 0.0, delta=tolerance)
        self.assertAlmostEqual(declination_angle(datetime(2001, 10, 21, 00, 00, 00)).degrees, -10.5, delta=tolerance)
        self.assertAlmostEqual(declination_angle(datetime(2001, 11, 21, 00, 00, 00)).degrees, -19.8, delta=tolerance)
        self.assertAlmostEqual(declination_angle(datetime(2001, 12, 21, 00, 00, 00)).degrees, -23.5, delta=tolerance)


class TestLocalCivilTime(TestCase):

    # validation from example 6-1 of the 5th Edition of McQuiston
    def test_example_5_6_1(self):
        dt = datetime(2001, 2, 21, 11, 00, 00)
        dst_on = True
        longitude = Angular(degrees=95)
        standard_meridian = Angular(degrees=90)
        self.assertAlmostEqual(local_civil_time(dt, dst_on, longitude, standard_meridian), 9.67, delta=0.01)


class TestLocalSolarTime(TestCase):

    # validation from example 6-1 of the 5th Edition of McQuiston
    def test_example_5_6_1(self):
        dt = datetime(2001, 2, 21, 11, 00, 00)
        dst_on = True
        longitude = Angular(degrees=95)
        standard_meridian = Angular(degrees=90)
        self.assertAlmostEqual(local_solar_time(dt, dst_on, longitude, standard_meridian), 9.43, delta=0.01)


class TestHourAngle(TestCase):

    # validation from example 6-2 of the 5th Edition of McQuiston
    def test_example_5_6_2(self):
        dt = datetime(2001, 7, 21, 10, 00, 00)
        dst_on = True
        longitude = Angular(degrees=85)
        standard_meridian = Angular(degrees=90)
        self.assertAlmostEqual(local_civil_time(dt, dst_on, longitude, standard_meridian), 9.3, delta=0.1)
        self.assertAlmostEqual(equation_of_time(dt), -6.2, delta=0.2)
        self.assertAlmostEqual(local_solar_time(dt, dst_on, longitude, standard_meridian), 9.23, delta=0.01)
        self.assertAlmostEqual(hour_angle(dt, dst_on, longitude, standard_meridian).degrees, -41.5,
                               delta=0.1)  # we are using negative in the morning; positive in the afternoon

    # test solar_angles noon on standard meridian, should be zero right?
    def test_solar_noon(self):
        # chose June 15 because EOT goes near zero on that date
        dt = datetime(2001, 6, 15, 12, 0, 0)
        dst_on = False
        longitude = Angular(degrees=90)
        standard_meridian = Angular(degrees=90)
        self.assertAlmostEqual(hour_angle(dt, dst_on, longitude, standard_meridian).degrees, 0, delta=0.1)


class TestAltitudeAngle(TestCase):

    # validation from example 6-2 of the 5th Edition of McQuiston
    def test_example_5_6_2(self):
        dt = datetime(2001, 7, 21, 10, 00, 00)
        dst_on = True
        longitude = Angular(degrees=85)
        standard_meridian = Angular(degrees=90)
        latitude = Angular(degrees=40)
        self.assertAlmostEqual(altitude_angle(dt, dst_on, longitude, standard_meridian, latitude).degrees, 49.7,
                               delta=0.1)


class TestAzimuthAngle(TestCase):

    # validation from example 6-2 of the 5th Edition of McQuiston
    def test_example_5_6_2(self):
        dt = datetime(2001, 7, 21, 10, 00, 00)
        dst_on = True
        longitude = Angular(degrees=85)
        standard_meridian = Angular(degrees=90)
        latitude = Angular(degrees=40)
        expected_azimuth_from_south = Angular(degrees=73.7)
        expected_azimuth_from_north = 180 - expected_azimuth_from_south.degrees
        self.assertAlmostEqual(azimuth_angle(dt, dst_on, longitude, standard_meridian, latitude).degrees,
                               expected_azimuth_from_north, delta=0.1)

    # test one with the sun down to get a null-ish response
    def test_sun_is_down(self):
        dt = datetime(2001, 3, 21, 22, 00, 00)
        dst_on = True
        longitude = Angular(degrees=85)
        standard_meridian = Angular(degrees=90)
        latitude = Angular(degrees=40)
        self.assertFalse(azimuth_angle(dt, dst_on, longitude, standard_meridian, latitude).valued)


class TestWallAzimuthAngle(TestCase):

    # test east facing wall where the solar_angles azimuth is known from a prior unit test
    def test_gamma_south_facing(self):
        dt = datetime(2001, 7, 21, 10, 00, 00)
        dst_on = True
        longitude = Angular(degrees=85)
        standard_meridian = Angular(degrees=90)
        latitude = Angular(degrees=40)
        wall_normal = Angular(degrees=90)
        expected_solar_azimuth = 180 - 73.7
        expected_wall_azimuth = expected_solar_azimuth - wall_normal.degrees
        self.assertAlmostEqual(wall_azimuth_angle(dt, dst_on, longitude, standard_meridian, latitude, wall_normal).degrees,
                               expected_wall_azimuth, delta=0.1)

    # test one with the sun down to get a null-ish response
    def test_sun_is_down(self):
        dt = datetime(2001, 3, 21, 22, 00, 00)
        dst_on = True
        longitude = Angular(degrees=85)
        standard_meridian = Angular(degrees=90)
        latitude = Angular(degrees=40)
        wall_normal = Angular(degrees=90)
        self.assertFalse(wall_azimuth_angle(dt, dst_on, longitude, standard_meridian, latitude, wall_normal).valued)


class TestSolarAngleOfIncidence(TestCase):

    # test east facing surface where solar_angles azimuth and altitude are known from prior unit tests
    def test_theta_south_facing(self):
        dt = datetime(2001, 7, 21, 10, 00, 00)
        dst_on = True
        longitude = Angular(degrees=85)
        standard_meridian = Angular(degrees=90)
        latitude = Angular(degrees=40)
        wall_normal = Angular(degrees=90)
        expected_solar_azimuth = 180 - 73.7
        expected_wall_azimuth = radians(expected_solar_azimuth - wall_normal.degrees)
        expected_solar_altitude = radians(49.7)
        expected_theta = acos(cos(expected_wall_azimuth) * cos(expected_solar_altitude))
        angle = solar_angle_of_incidence(dt, dst_on, longitude, standard_meridian, latitude, wall_normal).radians
        self.assertAlmostEqual(angle, expected_theta, delta=0.001)

    # test case for azimuth specified greater than 360
    def test_over_rotated_surface(self):
        dt = datetime(2001, 7, 21, 10, 00, 00)
        dst_on = True
        longitude = Angular(degrees=85)
        standard_meridian = Angular(degrees=90)
        latitude = Angular(degrees=40)
        wall_normal = Angular(degrees=90)  # south, degrees
        base_theta = solar_angle_of_incidence(dt, dst_on, longitude, standard_meridian, latitude, wall_normal).radians
        wall_normal = Angular(degrees=90+360)  # south, degrees
        over_rotated_theta = solar_angle_of_incidence(dt, dst_on, longitude, standard_meridian, latitude,
                                                      wall_normal).radians
        self.assertAlmostEqual(over_rotated_theta, base_theta, delta=0.001)

    # test one with the sun down to get a null-ish response
    def test_sun_is_down(self):
        dt = datetime(2001, 3, 21, 22, 00, 00)
        dst_on = True
        longitude = Angular(degrees=85)
        standard_meridian = Angular(degrees=90)
        latitude = Angular(degrees=40)
        wall_normal = Angular(degrees=90)  # north, degrees
        self.assertFalse(
            solar_angle_of_incidence(dt, dst_on, longitude, standard_meridian, latitude, wall_normal).valued
        )


class TestRadiationOnSurface(TestCase):

    def test_direct_radiation_on_surface_south_facing(self):
        dt = datetime(2001, 7, 21, 10, 00, 00)
        dst_on = True
        longitude = Angular(degrees=85)
        standard_meridian = Angular(degrees=90)
        latitude = Angular(degrees=40)
        wall_normal = Angular(degrees=180)  # south, degrees
        theta = solar_angle_of_incidence(dt, dst_on, longitude, standard_meridian, latitude, wall_normal).radians
        insolation = 293  # watts
        self.assertAlmostEqual(
            direct_radiation_on_surface(dt, dst_on, longitude, standard_meridian, latitude, wall_normal, insolation),
            insolation * cos(theta), delta=0.1)
