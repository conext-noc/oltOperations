####################             IN MAINTANCE             ####################
import ipaddress
import re


data = """
---
  F/S/P                   : 0/3/14
  ONT-ID                  : 17
  Control flag            : active
  Run state               : offline
  Config state            : initial
  Match state             : initial
  DBA type                : SR
  ONT distance(m)         : -
  ONT last distance(m)    : 15813
  ONT battery state       : -
  ONT power type          : -
  Memory occupation       : -
  CPU occupation          : -
  Temperature             : -
  Authentic type          : SN-auth
  SN                      : 48575443B1E211A4 (HWTC-B1E211A4)
  Management mode         : OMCI
  Software work mode      : normal
  Isolation state         : normal
  ONT IP 0 address/mask   : -
  ONT IP 2 address/mask   : -
  Description             : ELENY MONTERO 0000007851
  Last down cause         : dying-gasp
  Last up time            : 2023-12-25 19:51:20-04:00
  Last down time          : 2023-12-30 09:15:32-04:00
  Last dying gasp time    : 2023-12-30 09:15:32-04:00
  ONT online duration     : -
  ONT system up duration  : -
  Type C support          : Not support
  Interoperability-mode   : Unknown
  Power reduction status  : -
  ONT NNI type            : auto
  ONT actual NNI type     : -
  Last ONT actual NNI type: 2.5G/1.25G
  FEC upstream state      : use-profile-config
  VS-ID                   : 0
  VS name                 : admin-vs
  Global ONT-ID           : 17
"""

ont_ips = {f"ONT IP {x} address/mask": None for x in range(1, 3)}

ip_matches = re.findall(r"ONT IP (\d) address/mask\s*:\s*(.+)", data)

for match in ip_matches:
    ont_ips[f"ONT IP {match[0]} address/mask"] = match[1]

ip_addr = [ip for ip in ont_ips.values() if ip is not None and "-" != ip]

network = ipaddress.IPv4Network(ip_addr[0] if len(ip_addr) > 0 else '0.0.0.0/0', strict=False)

# Get the IP address and subnet mask
ip_address = network.network_address
subnet_mask = network.netmask

print(f"IP Address: {ip_address}")
print(f"Subnet Mask: {subnet_mask}")


####################             IN MAINTANCE             ####################
