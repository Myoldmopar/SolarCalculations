# SolarCalculations
This is a collection of solar angle and related calculations.

## Source
These are based mostly on Chapter 6 of _Heating, Ventilation, and Air Conditioning_ by Faye McQuistion and Jerald Parker, 3rd Edition, 1988.  Other sources are noted in the source.  All the functions were written from scratch by me.

## Documentation
The functions are all documented with Markdown syntax doc strings.  These can be easily viewed in a terminal from the root of the repository with `pydoc ./solar/solar.py`.  I am trying to get Sphinx to generate the docs in styled fashion as well.

## Testing
The source is tested using the python unittest framework.  To execute all the unit tests, just execute the test file (since it calls `unittest.main()`): `python test/test_solar.py`.  I still have several more unit tests to add.
