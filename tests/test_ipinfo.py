import os
import sys
import time
import unittest

current_directory = os.getcwd()
sys.path.append(current_directory)

from helpers.constants.definitions import olt_devices, endpoints
from helpers.utils.ssh import ssh
from helpers.handlers.request import db_request
from helpers.utils.decoder import check_iter, decoder, check
from netaddr import valid_ipv4
import ipaddress

ONT = {"frame": 0, "slot": 1, "port": 2, "id": 0}
OLT = "1"
DEBUG = True
NAME = "rick"
PAYLOAD = {
    "lookup_type": "D",
    "lookup_value": {
        "fspi": f"{ONT['frame']}/{ONT['slot']}/{ONT['port']}/{ONT['id']}",
        "olt": OLT,
    },
}
IPS = " address/mask   : "
IP_MASK_LEN = 18

class TestIpExtraction(unittest.TestCase):
    def test_wan_values(self):
        (comm, command, quit_ssh) = ssh(olt_devices[OLT], DEBUG)
        req = db_request(endpoints["get_client"], PAYLOAD)
        client = req["data"]
        command(
            f"display ont info {client['frame']} {client['slot']} {client['port']} {client['onu_id']}"
        )
        time.sleep(3)
        value = decoder(comm)
        
        ont_net = []
        ips = check_iter(value, IPS)
        for ip in ips:
            (addr_stop, _) = check(value[ip[1]:ip[1] + IP_MASK_LEN], r'\n').span()
            ont_ip = value[ip[1]:ip[1] + addr_stop]
            if ont_ip.find("-") < 0:
                ip = ont_ip.replace("\r", "")[:-3]
                mask = str(ipaddress.IPv4Network(ont_ip.replace("\r", ""), strict=False).netmask)
                ont_net.append(ip)
                ont_net.append(mask)
        print(ont_net)
        self.assertTrue(valid_ipv4(ont_net[0]))
        pass


if __name__ == "__main__":
    unittest.main()
