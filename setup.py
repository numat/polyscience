from setuptools import setup

setup(
    name="vwr",
    version="0.1.4",
    description="Python driver for VWR circulating baths.",
    url="http://github.com/numat/vwr/",
    author="Patrick Fuller",
    author_email="pat@numat-tech.com",
    packages=["vwr"],
    package_data={"vwr": ["vwr/client.js", "vwr/main.css",
                          "vwr/*.template"]},
    include_package_data=True,
    install_requires=["tornado", "blessings"],
    entry_points={
        "console_scripts": [("vwr = vwr:command_line")]
    },
    license="GPLv2",
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Development Status :: 4 - Beta",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.4",
        "Topic :: Scientific/Engineering :: Human Machine Interfaces",
        "Topic :: Scientific/Engineering :: Electronic Design Automation (EDA)"
    ]
)
