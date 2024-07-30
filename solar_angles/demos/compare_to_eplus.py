from datetime import datetime
import csv

from solar_angles.solar import hour_angle, altitude_angle, azimuth_angle, solar_angle_of_incidence

# Golden, CO
longitude = 104.85
standard_meridian = 105
latitude = 39.57

with open('/tmp/compare_winter_angles_library.csv', 'w') as csvfile:
    my_writer = csv.writer(csvfile)
    my_writer.writerow(['Hour', 'Hour Angle', 'Solar Altitude', 'Solar Azimuth'])
    for hour in range(0, 24):  # gives zero-based hours as expected in the datetime constructor
        x = hour
        dt = datetime(2001, 12, 21, hour, 30, 00)
        t_hour = hour_angle(dt, False, longitude, standard_meridian).degrees
        altitude = altitude_angle(dt, False, longitude, standard_meridian, latitude).degrees
        azimuth = azimuth_angle(dt, False, longitude, standard_meridian, latitude).degrees
        my_writer.writerow([x, -t_hour, altitude, azimuth])

with open('/tmp/compare_summer_angles_library.csv', 'w') as csvfile:
    my_writer = csv.writer(csvfile)
    my_writer.writerow(['Hour', 'Hour Angle', 'Solar Altitude', 'Solar Azimuth'])
    for hour in range(0, 24):  # gives zero-based hours as expected in the datetime constructor
        x = hour
        dt = datetime(2001, 7, 21, hour, 30, 00)
        t_hour = hour_angle(dt, False, longitude, standard_meridian).degrees
        altitude = altitude_angle(dt, False, longitude, standard_meridian, latitude).degrees
        azimuth = azimuth_angle(dt, False, longitude, standard_meridian, latitude).degrees
        my_writer.writerow([x, -t_hour, altitude, azimuth])

with open('/tmp/compare_summer_incidence_library.csv', 'w') as csvfile:
    my_writer = csv.writer(csvfile)
    my_writer.writerow(['Hour', 'East Incidence', 'West Incidence'])
    for hour in range(0, 24):  # gives zero-based hours as expected in the datetime constructor
        x = hour
        dt = datetime(2001, 7, 21, hour, 30, 00)
        theta_west = solar_angle_of_incidence(
            dt, False, longitude, standard_meridian, latitude, 270).degrees
        theta_east = solar_angle_of_incidence(
            dt, False, longitude, standard_meridian, latitude, 90).degrees
        my_writer.writerow([x, theta_east, theta_west])
