import re
import time
from helpers.utils.decoder import check_iter, decoder
import ipaddress

def wan_data(comm, command, client):
    ont_net = ["", ""]
    command(
        f"display ont info {client['frame']} {client['slot']} {client['port']} {client['onu_id']} | no-more"
    )
    time.sleep(3)

    output = decoder(comm)

    regex = check_iter(
        output,
        "--------------------------------------------------------------------------",
    )
    if len(regex) > 0:
        (_, start) = regex[0]
        (end, _) = regex[1]

        ont_section = output[start:end]

        ont_ips = {f"ONT IP {x} address/mask": None for x in range(1, 3)}

        ip_matches = re.findall(r"ONT IP (\d) address/mask\s*:\s*(.+)", ont_section)

        for match in ip_matches:
            ont_ips[f"ONT IP {match[0]} address/mask"] = match[1]

        ip_addr = [ip for ip in ont_ips.values() if ip is not None and "-" != ip]

        network = ipaddress.IPv4Network(
            ip_addr[0] if len(ip_addr) > 0 else "0.0.0.0/0", strict=False
        )

        # Get the IP address and subnet mask
        ont_net[0] = network.network_address
        ont_net[1] = network.netmask

    return ont_net
