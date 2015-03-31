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
        self.sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.listener = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.listener.bind(("", 1026))
        self.listener.settimeout(timeout)

    def turn_on(self):
        """Turns the circulating bath on.

        Returns:
            True if successful, else False.
        """
        self._send("SO1P{}".format(self.password))
        return (self._receive() == "!")

    def turn_off(self):
        """Turns the circulating bath off.

        Returns:
            True if successful, else False.
        """
        self._send("SO0P{}".format(self.password))
        return (self._receive() == "!")

    def get_setpoint(self):
        """Get the setpoint temperature."""
        self._send("RS")
        return float(self._receive())

    def get_temperature_units(self):
        """Gets the temperature units, e.g. C or F."""
        self._send("RU")
        return self._receive()

    def get_internal_temperature(self):
        """Get the temperature inside the bath."""
        self._send("RT")
        return float(self._receive())

    def get_external_temperature(self):
        """If connected, get the temperature of the external thermocouple."""
        self._send("RR")
        return self._receive()

    def set_setpoint(self, setpoint):
        """Sets setpoint temperature.

        Args:
            setpoint: Setpoint temperature, in machine units, as a float.
        Returns:
            True if successful, else False.
        """
        self._send("SS{:.2f}P{:d}".format(setpoint, self.password))
        return (self._receive() == "!")

    def close(self):
        """Closes the listening port."""
        self.listener.close()

    def _send(self, message):
        """Selds a message to the circulating bath."""
        self.sender.sendto((message + "\r").encode("utf-8"),
                           (self.address, 1024))

    def _receive(self):
        """Receives messages from the circulating bath."""
        message, _ = self.listener.recvfrom(512)
        return message.decode("utf-8").strip()
