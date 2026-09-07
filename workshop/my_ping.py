#!/bin/python3
import platform
import subprocess
from tqdm import tqdm

ip_succ = []
ip_fail = []
ip_list = []


def ping(p):
    param = '-n' if platform.system() == 'Windows' else '-c'
    command = ['ping', param, '1', p, '-W', '1']
    # execute cmd
    res = subprocess.call(command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    if res == 0:
        # (f"Ping {p} succeeded")
        ip_succ.append(p)
    else:
        ip_fail.append(p)
        # print(f"Ping {ip} failed")


def single_ping(base_ip, start, end):
    #build the cmd and return ips
    ip_list.clear()
    start = int(start)
    end = int(end)
    for i in tqdm(range(start, end)):
        ip = f"{base_ip}.{str(i)}"
        ping(ip)
    ip_list.append(ip_succ)
    ip_list.append(ip_fail)
    return ip_list

def multi_ping(ip, cidr):
    #build the cmd and return ips
    ip_list.clear()
    ip_succ.clear()
    ip_fail.clear()
    ip_split = ip.split('.')
    s = int(ip_split[1])
    t = int(ip_split[2])
    f = int(ip_split[3])

    f_dict = {'31': [f+1, f+2], '30': [f+1, f+3], '29': [f+1, f+7], '28': [f+1, f+15], '27': [f+1, f+31], '26': [f+1, f+63], '25': [f+1, f+127], '24': [f+1, f+255]}
    t_dict = {'23': [t+1, t+2], '22': [t+1, t+3], '21': [t+1, t+7], '20': [t+1, t+15], '19': [t+1, t+31], '18': [t+1, t+63], '17': [t+1, t+127], '16': [t+1, t+255]}
    s_dict = {'15': [s+1, s+2], '14': [s+1, s+3], '13': [s+1, s+7], '12': [s+1, s+15], '11': [s+1, s+31], '10': [s+1, s+63], '9': [s+1, s+127], '8': [s+1, s+255]}

    if int(cidr) > 23:
        base_ip = f"{ip_split[0]}.{ip_split[1]}.{ip_split[2]}"
        print(f_dict[cidr])
        for i in tqdm(range(f_dict[cidr][0], f_dict[cidr][1])):
            fin = f"{base_ip}.{str(i)}"
            ping(fin)

    if 15 < int(cidr) < 24:
        base_ip = f"{ip_split[0]}.{ip_split[1]}"
        for i in tqdm(range(t_dict[cidr][0], t_dict[cidr][1])):
            for j in range(1, 255):
                fin = f"{base_ip}.{str(i)}.{str(j)}"
                ping(fin)

    if 8 < int(cidr) < 16:
        base_ip = f"{ip_split[0]}"
        for i in tqdm(range(s_dict[cidr][0], s_dict[cidr][1])):
            for j in range(1, 255):
                for k in range(1, 255):
                    fin = f"{base_ip}.{str(i)}.{str(j)}.{str(k)}"
                    ping(fin)

    ip_list.append(ip_succ)
    ip_list.append(ip_fail)
    return ip_list


#run
#ping(input("Enter first 3 octets of IP range: "), input("range start: "), input("range end: "))
#print(ip_list)
