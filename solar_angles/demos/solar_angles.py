from datetime import datetime

from solar_angles import solar

# import the plotting library for demonstration -- pip install matplotlib should suffice
import matplotlib.pyplot as plt

# calculate times in Stillwater, OK -- to demonstrate the effect of longitude not lining up with the standard meridian
longitude = 97.05
standard_meridian = 90
latitude = 36.11
x = []
lct = []
lst = []
for hour in range(0, 24):  # gives zero-based hours as expected in the datetime constructor
    x.append(hour)
    dt = datetime(2001, 6, 21, hour, 00, 00)
    lct.append(solar.local_civil_time(dt, True, longitude, standard_meridian))
    lst.append(solar.local_solar_time(dt, True, longitude, standard_meridian))

plt.plot(x, 'black', label='Clock Time')
plt.plot(x, lct, 'grey', label='Civil Time', linewidth=6)
plt.plot(x, lst, 'yellow', label='Solar Time')
plt.xlim([0, 23])
plt.suptitle("Time Values for Stillwater, OK on June 21", fontsize=14, fontweight='bold')
plt.xlabel("Hour of Day -- Clock Time")
plt.ylabel("Time [hours]")
plt.grid(True, axis='both')
plt.legend()
plt.savefig('/tmp/DemoSolarAnglesCivilSolarTime.png')

# reset
plt.close()

# calculate hour angle for a summer day in Golden, CO
longitude = 105.2
standard_meridian = 105
latitude = 39.75
x = []
hours = []
for hour in range(0, 24):  # gives zero-based hours as expected in the datetime constructor
    x.append(hour)
    dt = datetime(2001, 6, 21, hour, 00, 00)
    hours.append(solar.hour_angle(dt, True, longitude, standard_meridian).degrees)

plt.plot(x, hours, 'b', label='Hour Angle')
plt.xlim([0, 23])
plt.suptitle("Hour Angle", fontsize=14, fontweight='bold')
plt.xlabel("Hour of Day -- Clock Time")
plt.ylabel("Angle [degrees]")
plt.grid(True, axis='both')
plt.legend()
plt.savefig('/tmp/DemoSolarAnglesHour.png')

# reset
plt.close()

# calculate solar_angles altitude angles for Winter and Summer days in Golden, CO
longitude = 105.2
standard_meridian = 105
latitude = 39.75
x = []
beta_winter = []
beta_summer = []
for hour in range(0, 24):  # gives zero-based hours as expected in the datetime constructor
    x.append(hour)
    dt = datetime(2001, 12, 21, hour, 00, 00)
    beta_winter.append(solar.altitude_angle(dt, False, longitude, standard_meridian, latitude).degrees)
    dt = datetime(2001, 6, 21, hour, 00, 00)
    beta_summer.append(solar.altitude_angle(dt, True, longitude, standard_meridian, latitude).degrees)

plt.plot(x, beta_winter, 'b', label='Winter')
plt.plot(x, beta_summer, 'r', label='Summer')
plt.xlim([0, 23])
plt.suptitle("Solar Altitude Angle", fontsize=14, fontweight='bold')
plt.xlabel("Hour of Day -- Clock Time")
plt.ylabel("Angle [degrees]")
plt.grid(True, axis='both')
plt.legend()
plt.savefig('/tmp/DemoSolarAngles1.png')

# reset
plt.close()

# calculate solar_angles azimuth angle for a summer day in Golden, CO
longitude = 105.2
standard_meridian = 105
latitude = 39.75
x = []
solar_az = []
for hour in range(0, 24):  # gives zero-based hours as expected in the datetime constructor
    x.append(hour)
    dt = datetime(2001, 6, 21, hour, 00, 00)
    solar_az.append(solar.azimuth_angle(dt, True, longitude, standard_meridian, latitude).degrees)

plt.plot(x, solar_az, 'b', label='Solar Azimuth Angle')
plt.xlim([0, 23])
plt.suptitle("Solar Azimuth Angle", fontsize=14, fontweight='bold')
plt.xlabel("Hour of Day -- Clock Time")
plt.ylabel("Angle [degrees]")
plt.grid(True, axis='both')
plt.legend()
plt.savefig('/tmp/DemoSolarAnglesSolarAzimuth.png')

# reset
plt.close()

# calculate wall azimuth angles for a summer day in Golden, CO
longitude = 105.2
standard_meridian = 105
latitude = 39.75
x = []
east_wall_normal_from_north = 90
east_az = []
south_wall_normal_from_north = 180
south_az = []
west_wall_normal_from_north = 270
west_az = []
for hour in range(0, 24):  # gives zero-based hours as expected in the datetime constructor
    x.append(hour)
    dt = datetime(2001, 6, 21, hour, 00, 00)
    east_az.append(
        solar.wall_azimuth_angle(dt, True, longitude, standard_meridian, latitude, east_wall_normal_from_north).degrees)
    south_az.append(solar.wall_azimuth_angle(dt, True, longitude, standard_meridian, latitude,
                                             south_wall_normal_from_north).degrees)
    west_az.append(
        solar.wall_azimuth_angle(dt, True, longitude, standard_meridian, latitude, west_wall_normal_from_north).degrees)

plt.plot(x, east_az, 'r', label='East Wall Azimuth Angle')
plt.plot(x, south_az, 'g', label='South Wall Azimuth Angle')
plt.plot(x, west_az, 'b', label='West Wall Azimuth Angle')
plt.xlim([0, 23])
plt.ylim([-90, 180])
plt.suptitle("Wall Azimuth Angles", fontsize=14, fontweight='bold')
plt.xlabel("Hour of Day -- Clock Time")
plt.ylabel("Angle [degrees]")
plt.grid(True, axis='both')
plt.legend()
plt.savefig('/tmp/DemoSolarAnglesWallAzimuths.png')

# reset
plt.close()

# calculate solar_angles angle of incidence for a summer day in Golden, CO
longitude = 105.2
standard_meridian = 105
latitude = 39.75
x = []
east_wall_normal_from_north = 90
east_theta = []
east_az = []
alt = []
for hour in range(0, 24):  # gives zero-based hours as expected in the datetime constructor
    x.append(hour)
    dt = datetime(2001, 6, 21, hour, 00, 00)
    east_az.append(
        solar.wall_azimuth_angle(dt, True, longitude, standard_meridian, latitude, east_wall_normal_from_north).degrees)
    east_theta.append(solar.solar_angle_of_incidence(dt, True, longitude, standard_meridian, latitude,
                                                     east_wall_normal_from_north).degrees)
    alt.append(solar.altitude_angle(dt, True, longitude, standard_meridian, latitude).degrees)

plt.plot(x, alt, 'r', label='Solar Altitude Angle')
plt.plot(x, east_az, 'g', label='East Wall Azimuth Angle')
plt.plot(x, east_theta, 'b', label='East Wall Incidence Angle')
plt.xlim([0, 23])
plt.ylim([-90, 180])
plt.suptitle("Wall Solar Incidence Angles", fontsize=14, fontweight='bold')
plt.xlabel("Hour of Day -- Clock Time")
plt.ylabel("Angle [degrees]")
plt.grid(True, axis='both')
plt.legend()
plt.savefig('/tmp/DemoSolarAnglesSolarIncidence.png')
