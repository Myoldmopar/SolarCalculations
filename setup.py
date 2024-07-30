from pathlib import Path
from setuptools import setup

from solar_angles import VERSION, PACKAGE_NAME
readme_file = Path(__file__).parent.resolve() / 'README.md'
readme_contents = readme_file.read_text()

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    packages=[PACKAGE_NAME],
    description="Quick solar_angles angle calculation package",
    package_data={},
    include_package_data=False,
    long_description=readme_contents,
    long_description_content_type='text/markdown',
    author='Edwin Lee',
    url='https://github.com/Myoldmopar/SolarCalculations',
    license='ModifiedBSD',
    install_requires=['matplotlib'],
    entry_points={
        'gui_scripts': [],
        'console_scripts': []},
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Physics',
        'Topic :: Utilities',
    ],
    platforms=[
        'Linux (Tested on Ubuntu)', 'MacOSX', 'Windows'
    ],
    keywords=[
        'Solar Angles',
        'Building Simulation', 'Whole Building Energy Simulation',
        'Heat Transfer', 'Modeling',
    ]
)
