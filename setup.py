"""Python driver for Polyscience circulating baths."""
from setuptools import setup

with open('README.md', 'r') as in_file:
    long_description = in_file.read()

setup(
    name='polyscience',
    version='0.1.16',
    description='Python driver for Polyscience circulating baths.',
    long_description=long_description,
    long_description_content_type='text/markdown',
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
        'Development Status :: 7 - Inactive',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering :: Human Machine Interfaces',
        'Topic :: Scientific/Engineering :: Electronic Design Automation (EDA)'
    ]
)
