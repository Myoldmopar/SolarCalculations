from datetime import datetime
import csv
import math
from calendar import monthrange

from solar_angles import solar


# in this validation, we switch the latitude and longitude midway through the year
def get_latitude(month: int) -> solar.Angular:
    if month <= 1:
        return solar.Angular(degrees=25.0)
    else:
        return solar.Angular(degrees=45.0)


def get_longitude(month: int) -> solar.Angular:
    if month <= 1:
        return solar.Angular(degrees=95.0)
    else:
        return solar.Angular(degrees=102.0)


standard_meridian = solar.Angular(degrees=105)
east_wall_normal_from_north = solar.Angular(degrees=90)
south_wall_normal_from_north = solar.Angular(degrees=180)
west_wall_normal_from_north = solar.Angular(degrees=270)
with open('/tmp/eplus_validation_location.csv', 'w') as csvfile:
    my_writer = csv.writer(csvfile)
    my_writer.writerow(
        ['Hour', 'Hour Angle', 'Solar Altitude', 'Solar Azimuth', 'Cos East Wall Theta', 'Cos South Wall Theta',
         'Cos West Wall Theta'])
    for month_num in range(1, 3):  # just january and february
        thisLat = get_latitude(month_num)
        thisLong = get_longitude(month_num)
        for day in range(1, monthrange(2011, month_num)[1] + 1):  # just make sure it isn't a leap year
            for hour in range(0, 24):  # gives zero-based hours as expected in the datetime constructor
                x = hour
                dt = datetime(2011, month_num, day, hour, 30, 00)
                t_hour = solar.hour_angle(dt, False, thisLong, standard_meridian).degrees()
                altitude = solar.altitude_angle(dt, False, thisLong, standard_meridian, thisLat).degrees()
                azimuth = solar.azimuth_angle(dt, False, thisLong, standard_meridian, thisLat).degrees()
                east_theta = solar.solar_angle_of_incidence(dt, False, thisLong, standard_meridian, thisLat,
                                                            east_wall_normal_from_north).radians()
                south_theta = solar.solar_angle_of_incidence(dt, False, thisLong, standard_meridian, thisLat,
                                                             south_wall_normal_from_north).radians()
                west_theta = solar.solar_angle_of_incidence(dt, False, thisLong, standard_meridian, thisLat,
                                                            west_wall_normal_from_north).radians()
                if east_theta is not None:
                    east_theta = math.cos(east_theta)
                if south_theta is not None:
                    south_theta = math.cos(south_theta)
                if west_theta is not None:
                    west_theta = math.cos(west_theta)
                my_writer.writerow([x, -t_hour, altitude, azimuth, east_theta, south_theta, west_theta])


def get_wall_orientation(month: int) -> solar.Angular:
    val = 0
    if month <= 1:
        val = 0
    elif month == 2:
        val = 90
    elif month == 3:
        val = 180
    elif month == 4:
        val = 270
    elif month == 5:
        val = 360
    return solar.Angular(degrees=val)


with open('/tmp/eplus_validation_orientation.csv', 'w') as csvfile:
    my_writer = csv.writer(csvfile)
    my_writer.writerow(['Month', 'Date', 'Hour', 'Hour Angle', 'Solar Altitude', 'Solar Azimuth', 'Cos Wall Theta'])
    for month_num in range(1, 7):  # just january through June to get all the way back through 360 and 0 again
        thisLat = solar.Angular(degrees=39.57)
        thisLong = solar.Angular(degrees=104.85)
        for day in range(1, monthrange(2011, month_num)[1] + 1):  # just make sure it isn't a leap year
            for hour in range(0, 24):  # gives zero-based hours as expected in the datetime constructor
                x = hour
                for minute in range(0,
                                    60):  # gives zero-based minutes, I think that's right...it should complain if not
                    dt = datetime(2011, month_num, day, hour, minute, 00)
                    t_hour = solar.hour_angle(dt, False, thisLong, standard_meridian).degrees()
                    altitude = solar.altitude_angle(dt, False, thisLong, standard_meridian, thisLat).degrees()
                    azimuth = solar.azimuth_angle(dt, False, thisLong, standard_meridian, thisLat).degrees()
                    wall_degrees_from_north = get_wall_orientation(month_num)
                    wall_theta = solar.solar_angle_of_incidence(dt, False, thisLong, standard_meridian, thisLat,
                                                                wall_degrees_from_north).radians()
                    if wall_theta is not None:
                        wall_theta = math.cos(wall_theta)
                    my_writer.writerow([month_num, day, x, -t_hour, altitude, azimuth, wall_theta])

with open('/tmp/quickcheck2.csv', 'w') as csvfile:
    my_writer = csv.writer(csvfile)
    my_writer.writerow(['Month', 'Date', 'Hour', 'Hour Angle', 'Solar Altitude', 'Solar Azimuth', 'Cos Wall Theta'])
    for month_num in range(1, 7):  # just january through June to get all the way back through 360 and 0 again
        thisLat = solar.Angular(degrees=25)
        thisLong = solar.Angular(degrees=95)
        for day in range(1, monthrange(2011, month_num)[1] + 1):  # just make sure it isn't a leap year
            for hour in range(0, 24):  # gives zero-based hours as expected in the datetime constructor
                x = hour
                for minute in range(0,
                                    60):  # gives zero-based minutes, I think that's right...it should complain if not
                    dt = datetime(2011, month_num, day, hour, minute, 00)
                    t_hour = solar.hour_angle(dt, False, thisLong, standard_meridian).degrees()
                    altitude = solar.altitude_angle(dt, False, thisLong, standard_meridian, thisLat).degrees()
                    azimuth = solar.azimuth_angle(dt, False, thisLong, standard_meridian, thisLat).degrees()
                    wall_degrees_from_north = solar.Angular(degrees=360)
                    wall_theta = solar.solar_angle_of_incidence(dt, False, thisLong, standard_meridian, thisLat,
                                                                wall_degrees_from_north).radians()
                    if wall_theta is not None:
                        wall_theta = math.cos(wall_theta)
                    my_writer.writerow([month_num, day, x, -t_hour, altitude, azimuth, wall_theta])
