import math
from datetime import datetime


# The calculations here are based on Chapter 6 of
# '   McQuiston, F.C. and J.D. Parker.  1998.
# '   Heating, Ventilating, and Air Conditioning Analysis and Design, Third Edition.
# '   John Wiley and Sons, New York.

# This was originally a class called SolarPosition, but that was actually a poor design
# The location is capable of moving each call, as well as the date/time.
# So there wasn't anything that needed to persist, and the arguments got funny between instantiation and function calls
# Thus it is just a little library of functions


class Angular:
    """
    This class combines a numeric value with an angular measurement unit.

    Proper construction should call constructor with either radians=x or degrees=y; not both.
    The constructor will calculate the complementary.
    The value of the angle can then be retrieved from the .degrees or .radians value as needed.

    Another class member, called .valued is available to determine if the class members contain meaningful values.

    If the constructor is called without either argument, the .valued variable is False, and the numeric vars are None.

    If the constructor is called with both arguments, they will be assigned if they agree to within a small tolerance;
    otherwise a ValueError is thrown.
    """

    def __init__(self, radians=None, degrees=None):
        """
        Constructor for the class.  Call it with either radians or degrees, not both.

        >>> a = Angular(radians=math.pi)
        >>> b = Angular(degrees=180)
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
        else:  # degrees and radians
            if abs(math.degrees(radians) - degrees) > 0.01:
                raise ValueError("Radians and Degrees both given but don't agree")
            self.valued = True
            self.radians = radians
            self.degrees = degrees

    def __str__(self) -> str:
        return f"{self.valued=}, {self.radians=}, {self.degrees=}"


def day_of_year(time_stamp: datetime) -> int:
    """
    Calculates the day of year (1-366) given a Python datetime.datetime instance.
    Basically a wrapper to ensure it is a full datetime instance .
    in subsequent calculations. If the type is *not* datetime.datetime, this will throw a TypeError.

    :param time_stamp: The current date and time to be used in calculating day of year
    :returns: [dimensionless] The day of year, from 1 to 365 for non-leap years and 1-366 for leap years.
    """
    if not type(time_stamp) is datetime:
        raise TypeError("Expected datetime.datetime type")
    return time_stamp.timetuple().tm_yday


def equation_of_time(time_stamp: datetime) -> float:
    """
    Calculates the Equation of Time for a given date.
    I wasn't able to get the McQuiston equation to match the values in the given table.
    I ended up using a different formulation here: http://holbert.faculty.asu.edu/eee463/SolarCalcs.pdf.

    :param time_stamp: The current date and time to be used in this calculation of day of year.
    :returns: The equation of time, which is the difference between local civil time and local solar time
    """
    degrees = (day_of_year(time_stamp) - 81.0) * (360.0 / 365.0)
    radians = math.radians(degrees)
    return 9.87 * math.sin(2 * radians) - 7.53 * math.cos(radians) - 1.5 * math.sin(radians)


def declination_angle(time_stamp: datetime) -> Angular:
    """
    Calculates the Solar Declination Angle for a given date.
    The solar declination angle is the angle between a line connecting the center of the sun and earth and the
    projection of that line on the equatorial plane. Calculation is based on McQuiston.

    :param time_stamp: The current date and time to be used in this calculation of day of year.
    :returns: The solar declination angle in an Angular with both radian and degree versions
    """
    radians = math.radians((day_of_year(time_stamp) - 1.0) * (360.0 / 365.0))
    dec_angle_deg = 0.3963723 - 22.9132745 * math.cos(radians) + 4.0254304 * math.sin(radians) - 0.387205 * math.cos(
        2.0 * radians) + 0.05196728 * math.sin(2.0 * radians) - 0.1545267 * math.cos(
        3.0 * radians) + 0.08479777 * math.sin(3.0 * radians)
    return Angular(degrees=dec_angle_deg)


def local_civil_time(time_stamp: datetime, daylight_savings_on: bool, longitude: Angular,
                     standard_meridian: Angular) -> float:
    """
    Calculates the local civil time for a given set of time and location conditions.
    The local civil time is the local time based on prime meridian and longitude.

    :param time_stamp: The current date and time to be used in this calculation of day of year.
    :param daylight_savings_on: A flag if the current time is a daylight savings number.
                                If True, the hour is decremented.
    :param longitude: [west] The current longitude, west of the prime meridian.
                      For Golden, CO, the variable should be = 105.2 degrees.
    :param standard_meridian: [west] The local standard meridian for the location, west
                              of the prime meridian.  For Golden, CO, the variable should be = 105 degrees.

    :returns: [hours] Returns the local civil time in hours for the given date/time/location
    """
    if not all([x.valued for x in [longitude, standard_meridian]]):
        raise ValueError("Invalid arguments to local_civil_time, must all be valid Angular objects")
    civil_hour = time_stamp.time().hour
    if daylight_savings_on:
        civil_hour -= 1
    local_civil_time_hours = civil_hour + time_stamp.time().minute / 60.0 + time_stamp.time().second / 3600.0 - 4 * (
            longitude.degrees - standard_meridian.degrees) / 60.0
    return local_civil_time_hours


def local_solar_time(time_stamp: datetime, daylight_savings_on: bool, longitude: Angular,
                     standard_meridian: Angular) -> float:
    """
    Calculates the local solar time for a given set of time and location conditions.
    The local solar time is the local civil time that has been corrected by the equation of time.

    :param time_stamp: The current date and time to be used in this calculation of day of year.
    :param daylight_savings_on: A flag if the current time is a daylight savings number.
                                If True, the hour is decremented.
    :param longitude: [west] The current longitude, west of the prime meridian.
                      For Golden, CO, the variable should be = 105.2 degrees.
    :param standard_meridian: [west] The local standard meridian for the location, west
                              of the prime meridian.  For Golden, CO, the variable should be = 105 degrees.

    :returns: [hours] Returns the local solar time in hours for the given date/time/location
    """
    if not all([x.valued for x in [longitude, standard_meridian]]):
        raise ValueError("Invalid arguments to local_solar_time, must all be valid Angular objects")
    return local_civil_time(
        time_stamp, daylight_savings_on, longitude, standard_meridian
    ) + equation_of_time(time_stamp) / 60.0


def hour_angle(time_stamp: datetime, daylight_savings_on: bool, longitude: Angular,
               standard_meridian: Angular) -> Angular:
    """
    Calculates the current hour angle for a given set of time and location conditions.
    The hour angle is the angle between solar noon and the current solar angle, so at local
    solar noon the value is zero, in the morning it is below zero, and in the afternoon it is positive.

    :param time_stamp: The current date and time to be used in this calculation of day of year.
    :param daylight_savings_on: A flag if the current time is a daylight savings number.
                                If True, the hour is decremented.
    :param longitude: [west] The current longitude west of the prime meridian.
                      For Golden, CO, the variable should be = 105.2 degrees.
    :param standard_meridian: [west] The local standard meridian for the location, west
                              of the prime meridian.  For Golden, CO, the variable should be = 105 degrees.

    :returns: The hour angle in an Angular with both radian and degree versions
    """
    if not all([x.valued for x in [longitude, standard_meridian]]):
        raise ValueError("Invalid arguments to hour_angle, must all be valid Angular objects")
    local_solar_time_hours = local_solar_time(time_stamp, daylight_savings_on, longitude, standard_meridian)
    hour_angle_deg = 15.0 * (local_solar_time_hours - 12)
    return Angular(degrees=hour_angle_deg)


def altitude_angle(time_stamp: datetime, daylight_savings_on: bool, longitude: Angular, standard_meridian: Angular,
                   latitude: Angular) -> Angular:
    """
    Calculates the current solar altitude angle for a given set of time and location conditions.
    The solar altitude angle is the angle between the sun rays and the horizontal plane.

    :param time_stamp: The current date and time to be used in this calculation of day of year.
    :param daylight_savings_on: A flag if the current time is a daylight savings number.
                                If True, the hour is decremented.
    :param longitude: [degrees west] The current longitude in degrees west of the prime meridian.
                      For Golden, CO, the variable should be = 105.2.
    :param standard_meridian: [west] The local standard meridian for the location, west
                              of the prime meridian.  For Golden, CO, the variable should be = 105 degrees.
    :param latitude: [north] The local latitude for the location, north of the equator.
                     For Golden, CO, the variable should be = 39.75 degrees.

    :returns: [Angular] The solar altitude angle in an Angular with both radian and degree versions
    """
    if not all([x.valued for x in [longitude, standard_meridian, latitude]]):
        raise ValueError("Invalid arguments to altitude_angle, must all be valid Angular objects")
    declination_radians = declination_angle(time_stamp).radians
    hour_radians = hour_angle(time_stamp, daylight_savings_on, longitude, standard_meridian).radians
    altitude_radians = math.asin(
        math.cos(latitude.radians) * math.cos(declination_radians) * math.cos(hour_radians) + math.sin(
            latitude.radians) * math.sin(declination_radians))
    return Angular(radians=altitude_radians)


def azimuth_angle(time_stamp: datetime, daylight_savings_on: bool, longitude: Angular, standard_meridian: Angular,
                  latitude: Angular) -> Angular:
    """
    Calculates the current solar azimuth angle for a given set of time and location conditions.
    The solar azimuth angle is the angle in the horizontal plane between due north and the sun.
    It is measured clockwise, so that east is +90 degrees and west is +270 degrees.

    :param time_stamp: The current date and time to be used in this calculation of day of year.
    :param daylight_savings_on: A flag if the current time is a daylight savings number.
                                If True, the hour is decremented.
    :param longitude: [west] The current longitude west of the prime meridian.
                      For Golden, CO, the variable should be = 105.2 degrees.
    :param standard_meridian: [west] The local standard meridian for the location, west
                              of the prime meridian.  For Golden, CO, the variable should be = 105 degrees.
    :param latitude: [north] The local latitude for the location, north of the equator.
                     For Golden, CO, the variable should be = 39.75 degrees.

    :returns: [Angular] The solar azimuth angle in an Angular with both radian and degree versions.
              NOTE: If the sun is down, the Float values in the dictionary are None.
    """
    if not all([x.valued for x in [longitude, standard_meridian, latitude]]):
        raise ValueError("Invalid arguments to azimuth_angle, must all be valid Angular objects")
    declination_radians = declination_angle(time_stamp).radians
    altitude = altitude_angle(time_stamp, daylight_savings_on, longitude, standard_meridian, latitude)
    if altitude.degrees < 0:  # sun is down
        return Angular()
    hour_radians = hour_angle(time_stamp, daylight_savings_on, longitude, standard_meridian).radians
    acos_from_south = math.acos(
        (math.sin(altitude.radians) * math.sin(latitude.radians) - math.sin(declination_radians)) / (
                math.cos(altitude.radians) * math.cos(latitude.radians)))
    if hour_radians < 0:
        azimuth_from_south = acos_from_south
    else:
        azimuth_from_south = -acos_from_south
    azimuth_angle_radians = math.radians(180) - azimuth_from_south
    return Angular(radians=azimuth_angle_radians)


def wall_azimuth_angle(time_stamp: datetime, daylight_savings_on: bool, longitude: Angular, standard_meridian: Angular,
                       latitude: Angular, surface_azimuth: Angular) -> Angular:
    """
    Calculates the current wall azimuth angle for a given set of time/location conditions, and a surface orientation.
    The wall azimuth angle is the angle in the horizontal plane between the solar azimuth
    and the vertical wall's outward facing normal vector.

    :param time_stamp: The current date and time to be used in this calculation of day of year.
    :param daylight_savings_on: A flag if the current time is a daylight savings number.
                                If True, the hour is decremented.
    :param longitude: [west] The current longitude west of the prime meridian.
                      For Golden, CO, the variable should be = 105.2 degrees.
    :param standard_meridian: [west] The local standard meridian for the location, west
                              of the prime meridian.  For Golden, CO, the variable should be = 105 degrees.
    :param latitude: [north] The local latitude for the location, north of the equator.
                     For Golden, CO, the variable should be = 39.75 degrees.
    :param surface_azimuth: [CW from North] The angle between north and the outward facing
                                normal vector of the wall, measured as positive clockwise from south
                                (southwest facing surface: 225 degrees, northwest facing surface: 315 degrees)

    :returns: [Angular] The wall azimuth angle in an Angular with both radian and degree versions.
              NOTE: If the sun is behind the surface, the Float values in the object are None.
    """
    if not all([x.valued for x in [longitude, standard_meridian, latitude, surface_azimuth]]):
        raise ValueError("Invalid arguments to wall_azimuth_angle, must all be valid Angular objects")
    this_surface_azimuth_deg = surface_azimuth.degrees % 360
    solar_azimuth = azimuth_angle(time_stamp, daylight_savings_on, longitude, standard_meridian, latitude).degrees
    if solar_azimuth is None:  # sun is down
        return Angular()
    wall_azimuth_degrees = solar_azimuth - this_surface_azimuth_deg
    if wall_azimuth_degrees > 90 or wall_azimuth_degrees < -90:
        return Angular()
    return Angular(degrees=wall_azimuth_degrees)


def solar_angle_of_incidence(time_stamp: datetime, daylight_savings_on: bool, longitude: Angular,
                             standard_meridian: Angular, latitude: Angular,
                             surface_azimuth: Angular) -> Angular:
    """
    Calculates the solar angle of incidence for a given set of time and location conditions, and a surface orientation.
    The solar angle of incidence is the angle between the solar ray vector incident on the surface,
    and the outward facing surface normal vector.

    :param time_stamp: The current date and time to be used in this calculation of day of year.
    :param daylight_savings_on: A flag if the current time is a daylight savings number.
                                If True, the hour is decremented.
    :param longitude: [west] The current longitude west of the prime meridian.
                      For Golden, CO, the variable should be = 105.2 degrees.
    :param standard_meridian: [west] The local standard meridian for the location, west
                              of the prime meridian.  For Golden, CO, the variable should be = 105 degrees.
    :param latitude: [north] The local latitude for the location, north of the equator.
                     For Golden, CO, the variable should be = 39.75 degrees.
    :param surface_azimuth: [CW from North] The angle between north and the outward facing
                                normal vector of the wall, measured as positive clockwise from south
                                (southwest facing surface: 225 degrees, northwest facing surface: 315 degrees)

    :returns: [Angular] The solar angle of incidence in an Angular with both radian & degree versions.
              NOTE: If the sun is down, or behind the surface, the Float values in the object are None.
    """
    if not all([x.valued for x in [longitude, standard_meridian, latitude, surface_azimuth]]):
        raise ValueError("Invalid arguments to solar_angle_of_incidence, must all be valid Angular objects")
    wall_azimuth_rad = wall_azimuth_angle(time_stamp, daylight_savings_on, longitude, standard_meridian, latitude,
                                          surface_azimuth).radians
    if wall_azimuth_rad is None:
        return Angular()
    altitude_rad = altitude_angle(time_stamp, daylight_savings_on, longitude, standard_meridian, latitude).radians
    incidence_angle_radians = math.acos(math.cos(altitude_rad) * math.cos(wall_azimuth_rad))
    return Angular(radians=incidence_angle_radians)


def direct_radiation_on_surface(time_stamp: datetime, daylight_savings_on: bool, longitude: Angular,
                                standard_meridian: Angular, latitude: Angular,
                                surface_azimuth: Angular, horizontal_direct_irradiation: float) -> float:
    """
    Calculates the amount of direct solar radiation incident on a surface for a set of time and location conditions,
    a surface orientation, and a total global horizontal direct irradiation. This is merely the global horizontal
    direct solar irradiation times the angle of incidence on the surface.

    :param time_stamp: The current date and time to be used in this calculation of day of year.
    :param daylight_savings_on: A flag if the current time is a daylight savings number.
                                If True, the hour is decremented.
    :param longitude: [west] The current longitude west of the prime meridian.
                      For Golden, CO, the variable should be = 105.2 degrees.
    :param standard_meridian: [west] The local standard meridian for the location, west
                              of the prime meridian.  For Golden, CO, the variable should be = 105 degrees.
    :param latitude: [north] The local latitude for the location, north of the equator.
                     For Golden, CO, the variable should be = 39.75 degrees.
    :param surface_azimuth: [CW from North] The angle between north and the outward facing
                                normal vector of the wall, measured as positive clockwise from south
                                (southwest facing surface: 225 degrees, northwest facing surface: 315 degrees)
    :param horizontal_direct_irradiation: The global horizontal direct irradiation at the location, in any units

    :returns: The incident direct radiation on the surface.
              The units of this return value match the units of the parameter :horizontal_direct_irradiation:
    """
    if not all([x.valued for x in [longitude, standard_meridian, latitude, surface_azimuth]]):
        raise ValueError("Invalid arguments to direct_radiation_on_surface, must all be valid Angular objects")
    theta = solar_angle_of_incidence(time_stamp, daylight_savings_on, longitude, standard_meridian, latitude,
                                     surface_azimuth).radians
    return horizontal_direct_irradiation * math.cos(theta)
