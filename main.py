#!/usr/bin/env python

import sys, subprocess

from SystemConfiguration import *

password = "112334556"

prefs = SCPreferencesCreate(None, 'foo', None)
network_services = SCNetworkServiceCopyAll(prefs)


def get_network_service_list():
    """Returns a list of network interfaces"""
    service_list = []
    for service in network_services:
        service_list.append(SCNetworkServiceGetName(service))
    return service_list


def set_config(service_list, argument, category):
    """Sets dns servers"""
    for service in service_list:
        if 'Wi-Fi' in service:
            cmd = 'echo {} | sudo -S /usr/sbin/networksetup {} "{}" {}'.format(password, argument,
                                                                               service, ' '.join(category))
            task = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            (out, err) = task.communicate()
            if err:
                print('Unable to set {}: {}'.format(category, err))
                sys.exit(1)


def main(dns):
    service_list = get_network_service_list()
    set_config(service_list, '-setdnsservers', dns)


if __name__ == "__main__":
    if not len(sys.argv) == 2:
        raise ValueError("Command line option required, either on or off")
    if sys.argv[1] == "on":
        dns_server = ["192.168.1.10"]
    elif sys.argv[1] == "off":
        dns_server = ["192.168.1.1"]
    else:
        raise ValueError("Value must be on or off")
    main(dns_server)

# alias dnsoff="/Users/bla/python_code/dns_switch/main.py off"
# alias dnson="/Users/bla/python_code/dns_switch/main.py on"
