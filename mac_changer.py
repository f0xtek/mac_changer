#!/usr/bin/env python3

import optparse
import re
import socket
import subprocess
import sys


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


def get_current_mac(interface):
    ifconfig_output = subprocess.check_output(["ifconfig", interface]).decode("utf-8")
    changed_mac = re.search(r"\w{2}:\w{2}:\w{2}:\w{2}:\w{2}:\w{2}", ifconfig_output)
    if changed_mac:
        return changed_mac.group(0)
    else:
        print(f"[-] Could not read MAC address from interface {interface}.")
        sys.exit(1)


def check_interfaces(interface):
    interfaces = socket.if_nameindex()
    available_interfaces = []
    for interface_set in interfaces:
        available_interfaces.append(interface_set[1])
    return interface in available_interfaces


options = get_arguments()

if not check_interfaces(options.interface):
    print(f"[-] Interface {options.interface} not found!")
    sys.exit(1)

current_mac = get_current_mac(options.interface)
print(f"[+] Current MAC: {current_mac}")

change_mac(options.interface, options.mac)
current_mac = get_current_mac(options.interface)

if str(current_mac) == options.mac:
    print(f"[+] MAC successfully changed to {current_mac}")
else:
    print("MAC address could not be changed!")
