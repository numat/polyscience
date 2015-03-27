vwr
===

UDP ethernet driver and command line tool for [VWR circulating baths](https://us.vwr.com/store/catalog/product.jsp?catalog_number=89203-002).

<p align="center">
  <img src="https://us.vwr.com/stibo/low_res/std.lang.all/53/83/7545383.jpg" height="400" />
</p>

Installation
============

```
pip install git+https://github.com/numat/vwr
```

If you don't like pip, you can also install from source:

```
git clone https://github.com/numat/vwr
cd vwr
python setup.py install
```

Usage
=====

###Command Line

To read and set temperatures, use the command line tool. Read the help for
more.

```
vwr --help
```

###Python

For complex interaction, use this as part of a Python script.

```python
from vwr import CirculatingBath
bath = CirculatingBath("192.168.1.100")
print(bath.get_setpoint())
```

Only some functionality is currently implemented. We will expand this in the
future.
