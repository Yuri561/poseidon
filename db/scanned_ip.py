import ipaddress

scanned_ips = {}

network = ipaddress.ip_network("10.6.16.165")

for ip in network.hosts():
    print(ip)