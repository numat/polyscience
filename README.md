polyscience
===========

Python driver for [Polyscience Advanced Digital Controller Circulating Baths](https://polyscience.com/products/circulating-baths/heated-circulators/integrated-heated-baths/advanced-digital-controller).

<p align="center">
  <img src="https://polyscience.com/sites/default/files/public/product-image/AD15H200.jpg" height="400" />
</p>

This was created to support older circulating baths (before touch screen models). These older devices have ethernet ports, but only support serial communication
over UDP. This code attempts to handle the awkwardness of serial-over-UDP communication, providing a simple API to read and control the unit.

Installation
============

```
pip install polyscience
```

If you don't like pip, you can also install from source:

```
git clone https://github.com/numat/polyscience
cd polyscience
python setup.py install
```

Usage
=====

### Command Line

Read the bath from any networked computer with:

```
polyscience [ip-address]
```

This provides methods to set temperature, pump speed, control, and others. See `polyscience --help` for more.

### Python

For complex interaction, use this as part of a Python script.

```python
from polyscience import CirculatingBath
bath = CirculatingBath('192.168.1.100')
print(bath.get_setpoint())
```

A common usage is to create an interactive web site. This driver blocks (my earlier async implementations were prone to overwhelming the bath), so put the bath i/o in its own thread.
