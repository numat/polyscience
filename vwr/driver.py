#!/usr/bin/env python
"""Python driver for [VWR circulating baths]
(https://us.vwr.com/store/catalog/product.jsp?catalog_number=89203-002).

Distributed under the GNU General Public License v2
Copyright (C) 2015 NuMat Technologies
"""
import socket


class CirculatingBath(object):
    """Python driver for [VWR circulating baths](https://us.vwr.com/store/
    catalog/product.jsp?catalog_number=89203-002).

    This class communicates with the circulating bath over UDP sockets.
    """
    def __init__(self, address, password=100, timeout=2):
        """Opens ports to communicate with the circulating bath.

        Args:
            address: The IP address of the device
            password: The password next to "Unlock" in the user interface
                settings. Default 100.
            timeout: Max time to wait for response, in seconds. Default 2.
        """
        self.address = address
        self.password = password
        self.timeout = timeout
        self.sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.listener = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.listener.bind(('', 1026))
        self.listener.settimeout(timeout)

    def turn_on(self):
        """Turns the circulating bath on.

        Returns:
            True if successful, else False.
        """
        self._send('SO1P{}'.format(self.password))
        return (self._receive() == '!')

    def turn_off(self, timeout=5):
        """Turns the circulating bath off.

        Note that turning the bath off takes multiple seconds before a response
        is sent. For this reason, this function has an independent `timeout`
        parameter.

        Returns:
            True if successful, else False.
        """
        self._send('SO0P{}'.format(self.password))
        self.listener.setttimeout(timeout)
        response = self._receive()
        self.listener.setttimeout(self.timeout)
        return (response == '!')

    def get(self):
        """Gets the setpoint and internal temperature."""
        return {'setpoint': self.get_setpoint(),
                'actual': self.get_internal_temperature(),
                'pump': self.get_pump_speed(),
                'on': self.get_operating_status()}

    def get_setpoint(self):
        """Gets the setpoint temperature."""
        self._send('RS')
        return float(self._receive())

    def get_temperature_units(self):
        """Gets the temperature units, e.g. C or F."""
        self._send('RU')
        return self._receive()

    def get_internal_temperature(self):
        """Gets the temperature inside the bath."""
        self._send('RT')
        return float(self._receive())

    def get_external_temperature(self):
        """If connected, get the temperature of the external thermocouple."""
        self._send('RR')
        return self._receive()

    def get_operating_status(self):
        """Returns a boolean indicating if bath is operating."""
        self._send('RO')
        return bool(int(self._receive()))

    def get_pump_speed(self):
        """Returns pump speed as an integer indicating percent, 5-100."""
        self._send('RM')
        return int(self._receive())

    def set_setpoint(self, setpoint):
        """Sets setpoint temperature.

        Args:
            setpoint: Setpoint temperature, in machine units, as a float.
        Returns:
            True if successful, else False.
        """
        self._send('SS{:.2f}P{:d}'.format(setpoint, self.password))
        return (self._receive() == '!')

    def set_pump_speed(self, speed):
        """Sets pump speed.

        Args:
            setpoint: Pump speed as an integer, 5-100. Will be rounded to
                nearest 5.
        Returns:
            True if successful, else False.
        """
        rounded_speed = int(5 * round(speed / 5))
        self._send('SM{:d}P{:d}'.format(rounded_speed, self.password))
        return (self._receive() == '!')

    def close(self):
        """Closes the listening port."""
        self.listener.close()

    def _send(self, message):
        """Selds a message to the circulating bath."""
        self.sender.sendto((message + '\r').encode('utf-8'),
                           (self.address, 1024))

    def _receive(self):
        """Receives messages from the circulating bath."""
        message, _ = self.listener.recvfrom(512)
        return message.decode('utf-8').strip()
