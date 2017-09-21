#!/usr/bin/env python
"""
Python driver and command-line tool for [Polyscience circulating
baths](https://polyscience.com/sites/default/files/public/product-image/
AD15H200.jpg).

Distributed under the GNU General Public License v2
Copyright (C) 2015 NuMat Technologies
"""
from polyscience.udp import CirculatingBath


def command_line():
    """Command-line interface to driver. Run with `polyscience`."""
    import argparse
    import json
    import sys

    parser = argparse.ArgumentParser(description="Control a Polyscience "
                                     "Advanced Digital Controller Circulating "
                                     "Bath from the command line.")
    parser.add_argument('address', help="The IP address of the bath.")
    parser.add_argument('--set-temperature', '-t', default=None, type=float,
                        help="Sets the bath temperature.")
    parser.add_argument('--set-pump-speed', '-p', default=None, type=float,
                        help="Sets the bath pump speed.")
    parser.add_argument('--unlock-code', '-u', default=100, type=int,
                        help="The code opposite the 'Unlock' option on the "
                        "circulating bath. Default 100.")
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--turn-on', '-on', action='store_true',
                       help="Turns device on.")
    group.add_argument('--turn-off', '-off', action='store_true',
                       help="Turns device off.")
    args = parser.parse_args()

    bath = CirculatingBath(args.address, password=args.unlock_code, timeout=5)

    try:
        if args.turn_on:
            bath.turn_on()
        if args.turn_off:
            bath.turn_off()
        if args.set_temperature:
            bath.set_setpoint(args.set_temperature)
        if args.set_pump_speed:
            bath.set_pump_speed(args.set_pump_speed)
        print(json.dumps(bath.get(), indent=4, sort_keys=True))
    except TimeoutError:
        sys.stderr.write("Could not connect to circulating bath. "
                         "Is it running at {}?\n".format(args.address))
        bath.close()


if __name__ == "__main__":
    command_line()
