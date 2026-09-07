#!/bin/python3
import platform
import subprocess

import ifaddr


def get_detailed_ips():
    adapters = ifaddr.get_adapters()
    ip_list = []

    for adapter in adapters:
        for ip in adapter.ips:
            # Filters out network prefixes, keeping the actual IP string
            if ip.is_IPv4:
                print(f"Interface: {adapter.nice_name}")
                print(f"   IPv4: {ip.ip}")
                ip_list.append(ip.ip)
           


    return ip_list


all_ips = get_detailed_ips()
