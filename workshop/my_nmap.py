#!/bin/python3
import subprocess
import nmap
from tqdm import tqdm
import my_ping
from my_ping import ip_list


# makes port scan object
nm = nmap.PortScanner()
#port_list = {}
#ip_list = ["10.149.100.1", "10.149.100.3", "10.149.100.5", "10.149.100.10"]
dev_info = {}

def my_nm(ip_list, option):
    global dev_info
    #ping for up hosts
    #my_ping.ping(input("Enter first 3 octets of IP range: "), input("range start: "), input("range end: "))
    #my_ping.ping(base, start, end)
    print(f"Scanning IPs: {ip_list}")
    print(f"option: {option}")
    #for host in nm.all_hosts():
    #Run a nmap port scan op ips decoverd with a ping sweep
    for targets in tqdm(ip_list, desc="Scanning IPs"):
        port_list = []
        nm.scan(hosts=targets, arguments=option)
        # noinspection DuplicatedCode
        print(targets)
        for host in nm.all_hosts():
            print(host)
            if nm[host].state() == 'up':
                # ADD ({nm[host].hostnames()}) before is up if you think nmap can do reverse dns did not work in testing but did not test long
                print(f"\nHost: {host}  is UP")
                # check for ports
                for proto in nm[host].all_protocols():
                    ports = nm[host][proto].keys()
                    for port in sorted(ports):
                        state = nm[host][proto][port]['state']
                        service = nm[host][proto][port]['name']
                        print(f" [+] Port: {port}/{proto}: {state} ({service})")
                        port_list.append(f"{port}/{proto} ({service})")

                info={
                    #"host": host,
                    "ports": port_list
                }
                dev_info[host] = info
                print(f" DEV INFO {dev_info}")
    print(dev_info)
    return dev_info

    # get a list of all hosts that are up
    #host_list = [(x, nm[x]['status']['state']) for x in nm.all_hosts()]



    #print(ip_list)
    #print(nm.all_hosts())
    #print(host_list)

    #for host, status in host_list:
    #    print(f'Host: {host} Status: {status}')

