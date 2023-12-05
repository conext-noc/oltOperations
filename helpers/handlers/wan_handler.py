import time
from helpers.utils.decoder import check_iter, decoder, check
import ipaddress


IPS = " address/mask   : "
IP_MASK_LEN = 18


def wan_data(comm, command, client):
    command(
        f"display ont info {client['frame']} {client['slot']} {client['port']} {client['onu_id']}"
    )
    time.sleep(3)
    value = decoder(comm)

    ont_net = ["",""]
    ips = check_iter(value, IPS)
    for ip in ips:
        (addr_stop, _) = check(value[ip[1] : ip[1] + IP_MASK_LEN], r"\n").span()
        ont_ip = value[ip[1] : ip[1] + addr_stop]
        if ont_ip.find("-") < 0:
            ip = ont_ip.replace("\r", "")[:-3]
            mask = str(
                ipaddress.IPv4Network(ont_ip.replace("\r", ""), strict=False).netmask
            )
            ont_net[0] = ip
            ont_net[1] = mask
    return ont_net
