from setuptools import setup

setup(
    name='polyscience',
    version='0.1.15',
    description='Python driver for Polyscience circulating baths.',
    url='http://github.com/numat/polyscience/',
    author='Patrick Fuller',
    author_email='pat@numat-tech.com',
    packages=['polyscience'],
    include_package_data=True,
    entry_points={
        'console_scripts': [('polyscience = polyscience:command_line')]
    },
    license='GPLv2',
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Development Status :: 4 - Beta',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering :: Human Machine Interfaces',
        'Topic :: Scientific/Engineering :: Electronic Design Automation (EDA)'
    ]
)
