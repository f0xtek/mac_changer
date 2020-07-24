#!/usr/bin/env python3

import optparse
import subprocess


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface name")
    parser.add_option("-m", "--mac", dest="mac", help="The new MAC address")
    (opts, args) = parser.parse_args()
    if not opts.interface:
        parser.error("Please specify an interface. See mac_changer.py -h for more info.")
    elif not opts.mac:
        parser.error("Please specify a mac address. See mac_changer.py -h for more info.")
    return opts


def change_mac(interface, new_mac):
    print(f"[+] Changing MAC address for {interface} to {new_mac}")
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])


options = get_arguments()
change_mac(options.interface, options.mac)
