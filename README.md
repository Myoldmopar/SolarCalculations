# SolarCalculations
This is a collection of solar angle and related calculations.
 
## Source
These are based mostly on Chapter 6 of _Heating, Ventilation, and Air Conditioning_ by Faye McQuistion and Jerald Parker, 3rd Edition, 1988, with minor pieces from other versions of the same book.  Other sources are noted in the source.  All the functions were written from scratch by me.

## Releases [![PyPIRelease](https://github.com/Myoldmopar/SolarCalculations/actions/workflows/release.yml/badge.svg)](https://github.com/Myoldmopar/SolarCalculations/actions/workflows/release.yml) ![PyPI - Version](https://img.shields.io/pypi/v/solar-angles?color=44cc11)
The latest release can be found on the [Releases](https://github.com/Myoldmopar/SolarCalculations/releases/latest) page.  All packages are distributed through [PyPi](https://pypi.org/project/solar-angles/).

## Documentation [![Documentation Status](https://readthedocs.org/projects/solarcalculations/badge/?version=latest)](https://solarcalculations.readthedocs.io/en/latest/?badge=latest)
Documentation is hosted on [ReadTheDocs](http://solar-calculations.readthedocs.org/en/latest/).  The functions are all documented with Markdown syntax doc strings in a way that Sphinx can interpret them.  To build the documentation, enter the docs/ subdirectory and execute `make html`; then open `/docs/_build/html/index.html` to see the documentation.

## Testing [![DevelopmentTest](https://github.com/Myoldmopar/SolarCalculations/actions/workflows/test.yml/badge.svg)](https://github.com/Myoldmopar/SolarCalculations/actions/workflows/test.yml) [![Flake8](https://github.com/Myoldmopar/SolarCalculations/actions/workflows/flake8.yml/badge.svg)](https://github.com/Myoldmopar/SolarCalculations/actions/workflows/flake8.yml) [![Coverage Status](https://coveralls.io/repos/github/Myoldmopar/SolarCalculations/badge.svg?branch=master)](https://coveralls.io/github/Myoldmopar/SolarCalculations?branch=master)
The source is tested using the python unittest framework.  To execute all the unit tests, just execute `coverage run -m pytest`.  The tests are run on each commit by GitHub [Actions](https://github.com/Myoldmopar/SolarCalculations/actions), and coverage results are pushed to [Coveralls](https://coveralls.io/github/Myoldmopar/SolarCalculations).  The goal is to be as close to 100% coverage as possible.

## Validation
The code has been carefully compared against numerous sampled points in the unit tests, and also [against EnergyPlus output](https://github.com/Myoldmopar/SolarCalculations/wiki/CompareToEnergyPlus), to ensure accurate values are being calculated.  If you find something wrong, just [file an issue](https://github.com/Myoldmopar/SolarCalculations/issues/new)!

## Demonstration
In order to show how to use the library, a [demonstration page](https://github.com/Myoldmopar/SolarCalculations/wiki/DemoSolarAngles) was created, that is based on the source in the [demos](https://github.com/Myoldmopar/SolarCalculations/tree/master/solar_angles/demos) folder.
