# import the datetime library so we construct proper datetime instances
from datetime import datetime

# import the plotting library for demonstration -- pip install matplotlib should suffice
import matplotlib.pyplot as plt

# import the solar_angles library
from solar_angles.solar import altitude_angle


def calculate_sun_up_time(array_of_altitude_angles):
    found_above_time = False
    last_alpha = None
    for index, alpha in enumerate(array_of_altitude_angles):
        if not found_above_time and alpha > 0:
            # we've got a match, calculate sun up and return
            sun_up_time = (index - 1) - (last_alpha / alpha) / (alpha - last_alpha)
            return sun_up_time
        else:
            last_alpha = alpha


def calculate_sun_down_time(array_of_altitude_angles):
    found_below_time = False
    last_alpha = None
    for index, alpha in enumerate(array_of_altitude_angles):
        if index < 12:
            continue
        if not found_below_time and alpha < 0:
            # we've got a match, calculate sun up and return
            sun_down_time = (index - 1) + (last_alpha / alpha) / (last_alpha + alpha)
            return sun_down_time
        else:
            last_alpha = alpha


# calculate times in Stillwater, OK -- to demonstrate the effect of longitude not lining up with the std meridian
longitude = 97.05
standard_meridian = 90
latitude = 36.11
x = []
for hour in range(0, 24):
    x.append(hour)

alpha0721 = []
for hour in range(0, 24):  # gives zero-based hours as expected in the datetime constructor
    dt = datetime(2001, 7, 21, hour, 00, 00)
    alpha0721.append(altitude_angle(dt, False, longitude, standard_meridian, latitude).degrees)

alpha0821 = []
for hour in range(0, 24):  # gives zero-based hours as expected in the datetime constructor
    dt = datetime(2001, 8, 21, hour, 00, 00)
    alpha0821.append(altitude_angle(dt, False, longitude, standard_meridian, latitude).degrees)

alpha0921 = []
for hour in range(0, 24):  # gives zero-based hours as expected in the datetime constructor
    dt = datetime(2001, 9, 21, hour, 00, 00)
    alpha0921.append(altitude_angle(dt, False, longitude, standard_meridian, latitude).degrees)

alpha1021 = []
for hour in range(0, 24):  # gives zero-based hours as expected in the datetime constructor
    dt = datetime(2001, 10, 21, hour, 00, 00)
    alpha1021.append(altitude_angle(dt, False, longitude, standard_meridian, latitude).degrees)

alpha1121 = []
for hour in range(0, 24):  # gives zero-based hours as expected in the datetime constructor
    dt = datetime(2001, 11, 21, hour, 00, 00)
    alpha1121.append(altitude_angle(dt, False, longitude, standard_meridian, latitude).degrees)

alpha1207 = []
for hour in range(0, 24):  # gives zero-based hours as expected in the datetime constructor
    dt = datetime(2001, 12, 7, hour, 00, 00)
    alpha1207.append(altitude_angle(dt, False, longitude, standard_meridian, latitude).degrees)

alpha1221 = []
for hour in range(0, 24):  # gives zero-based hours as expected in the datetime constructor
    dt = datetime(2001, 12, 21, hour, 00, 00)
    alpha1221.append(altitude_angle(dt, False, longitude, standard_meridian, latitude).degrees)

plt.plot(x, alpha0721, 'purple', label='7/21', linewidth=1)
plt.plot(x, alpha0821, 'blue', label='8/21', linewidth=1)
plt.plot(x, alpha0921, 'green', label='9/21', linewidth=1)
plt.plot(x, alpha1021, 'yellow', label='10/21', linewidth=1)
plt.plot(x, alpha1121, 'orange', label='11/21', linewidth=1)
plt.plot(x, alpha1207, 'red', label='12/7', linewidth=1)
plt.plot(x, alpha1221, 'black', label='12/21', linewidth=1)
plt.xlim([0, 23])
plt.ylim([0, 90])
plt.suptitle("Time Values for Stillwater", fontsize=14, fontweight='bold')
plt.xlabel("Hour of Day -- Clock Time")
plt.ylabel("Angle [degrees]")
plt.grid(True, axis='both')
plt.legend()
plt.savefig('/tmp/altitudes.png')
plt.close()

alpha1207 = []
for hour in range(0, 24):  # gives zero-based hours as expected in the datetime constructor
    dt = datetime(2001, 12, 7, hour, 00, 00)
    alpha1207.append(altitude_angle(dt, False, longitude, standard_meridian, latitude).degrees)

alpha1221 = []
for hour in range(0, 24):  # gives zero-based hours as expected in the datetime constructor
    dt = datetime(2001, 12, 21, hour, 00, 00)
    alpha1221.append(altitude_angle(dt, False, longitude, standard_meridian, latitude).degrees)

alpha0107 = []
for hour in range(0, 24):  # gives zero-based hours as expected in the datetime constructor
    dt = datetime(2001, 1, 7, hour, 00, 00)
    alpha0107.append(altitude_angle(dt, False, longitude, standard_meridian, latitude).degrees)

plt.plot(x, alpha1207, 'orange', label='12/7', linewidth=1)
plt.plot(x, alpha1221, 'black', label='12/21', linewidth=1)
plt.plot(x, alpha0107, 'red', label='1/7', linewidth=1)
plt.xlim([7, 18])
plt.ylim([0, 35])
plt.suptitle("Time Values for Stillwater", fontsize=14, fontweight='bold')
plt.xlabel("Hour of Day -- Clock Time")
plt.ylabel("Angle [degrees]")
plt.grid(True, axis='both')
plt.legend()
plt.savefig('/tmp/closeup.png')
plt.close()

sun_up_1207 = calculate_sun_up_time(alpha1207)
sun_up_1221 = calculate_sun_up_time(alpha1221)
sun_up_0107 = calculate_sun_up_time(alpha0107)
sun_down_1207 = calculate_sun_down_time(alpha1207)
sun_down_1221 = calculate_sun_down_time(alpha1221)
sun_down_0107 = calculate_sun_down_time(alpha0107)
print("Sun hours 12/07: %s" % (sun_down_1207 - sun_up_1207))
print("Sun hours 12/21: %s" % (sun_down_1221 - sun_up_1221))
print("Sun hours 01/07: %s" % (sun_down_0107 - sun_up_0107))
