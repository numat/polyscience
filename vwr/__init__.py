#!/usr/bin/env python
"""Python driver, command-line tool, and web server for [VWR circulating baths]
(https://us.vwr.com/store/catalog/product.jsp?catalog_number=89203-002).

Distributed under the GNU General Public License v2
Copyright (C) 2015 NuMat Technologies
"""
import argparse
import socket
import sys
from blessings import Terminal
from driver import CirculatingBath


def command_line():
    """Command-line interface to driver. Run with `vwr`."""
    parser = argparse.ArgumentParser(description="Control a VWR circulating "
                                     "bath from the command line, or run a "
                                     "web server.")
    parser.add_argument("address", help="The IP address of the bath.")
    parser.add_argument("--server", action="store_true", help="Runs "
                        "a web server for interfacing with the bath.")
    parser.add_argument("--password", "-p", default=100, type=int, help="The "
                        "password, as set through the bath interface. Default "
                        "100.")
    parser.add_argument("--set", "-s", default=None, type=float,
                        help="Sets the bath temperature.")
    parser.add_argument("--port", "-o", default=10000, type=int, help="The "
                        "port on which to run the web server. Default 10000.")
    args = parser.parse_args()

    bath = CirculatingBath(args.address, args.password)
    t = Terminal()

    try:
        units = bath.get_temperature_units()
    except socket.timeout:
        sys.stderr.write(t.bold_red("Could not connect to VWR circulating bath"
                         ". Is it running at {}?\r\n".format(args.address)))
        sys.exit(0)

    if args.set:
        success = bath.set_setpoint(args.set)
        if success:
            print(t.bold_green("Successfully set temperature to {setpoint:.2f}"
                  "°{units}.".format(setpoint=args.set, units=units)))
        else:
            sys.stderr.write(t.bold_red("Failed to set temperature."))

    if args.server:
        from server import run_server
        print(t.bold_white("Running server at http://localhost:{}/"
              .format(args.port)))
        run_server(bath, args.port)
    else:
        setpoint = bath.get_setpoint()
        actual = bath.get_internal_temperature()
        units = bath.get_temperature_units()
        print("Setpoint: {setpoint:.2f}°{units}\nActual: {actual:.2f}°{units}"
              .format(**locals()))
    bath.close()


if __name__ == "__main__":
    command_line()
