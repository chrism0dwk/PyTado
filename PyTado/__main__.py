#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Module for querying and controlling Tado smart thermostats."""

import argparse
import json
import logging
from PyTado.interface import Tado as tado_client
import sys
import time

def log_in(email, password):
    t = tado_client(email,password)
    return t

def get_me(args):
    t = log_in(args.email, args.password)
    me = tado_client.getMe(t)
    print(me)

def get_state(args):
    t = log_in(args.email, args.password)
    zone = tado_client.getState(t,int(args.zone))
    print(zone)

def get_capabilities(args):
    t = log_in(args.email, args.password)
    capabilities = tado_client.getCapabilities(t,int(args.zone))
    print(capabilities)

def main():
    """Main method for the script."""
    parser = argparse.ArgumentParser(description='Pytado - Tado thermostat device control',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    required_flags = parser.add_argument_group('required arguments')

    # Required flags go here.
    required_flags.add_argument('--email',
                                required=True,
                                help=('Tado username in the form of an email address.'))
    required_flags.add_argument('--password',
                                required=True,
                                help='Tado password.')

    # Flags with default values go here.
    loglevels = dict((logging.getLevelName(level), level) for level in [10, 20, 30, 40, 50])
    parser.add_argument('--loglevel',
                        default='INFO',
                        choices=list(loglevels.keys()),
                        help='Logging level to print to the console.')

    subparsers = parser.add_subparsers()

    show_config_parser = subparsers.add_parser('get_me', help='Get home information.')
    show_config_parser.set_defaults(func=get_me)

    start_activity_parser = subparsers.add_parser('get_state', help='Get state of zone.')
    start_activity_parser.add_argument('--zone', help='Zone to get the state of.')
    start_activity_parser.set_defaults(func=get_state)

    start_activity_parser = subparsers.add_parser('get_capabilities', help='Get capabilities of zone.')
    start_activity_parser.add_argument('--zone', help='Zone to get the capabilities of.')
    start_activity_parser.set_defaults(func=get_capabilities)

    args = parser.parse_args()

    logging.basicConfig(
        level=loglevels[args.loglevel],
        format='%(levelname)s:\t%(name)s\t%(message)s')

    sys.exit(args.func(args))

if __name__ == '__main__':
    main()
