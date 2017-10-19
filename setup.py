from distutils.core import setup

setup(
    name='hotwing-core',
    version='0.1.0',
    url='https://github.com/jasonhamilton/hotwing-core',
    packages=['hotwing_core','hotwing_core.cutting_strategies'],
    license='GPLv3',
    long_description="This Module which contains the core libraries for the HotWing-CLI and HotWing-GUI projects. "
                     "This Module provides a series of classes and functions to aid in creating GCode for 4-Axis CNC "
                     "foam cutters, specifically working with wing profiles, interpolating new profiles, and computing "
                     "reverse kinematics for the CNC.",
    keywords='development cnc gcode airfoil',
    classifiers=[

        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',

        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2',
        # 'Programming Language :: Python :: 2.6',
        # 'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        # 'Programming Language :: Python :: 3.2',
        # 'Programming Language :: Python :: 3.3',
        # 'Programming Language :: Python :: 3.4',
    ],
)