from time import sleep
from helpers.constants.regex_conditions import routers_ints, rtr_conflicts
from helpers.handlers.printer import log
from helpers.utils.decoder import decoder, check_iter
from helpers.handlers.interface import int_formatter
from helpers.handlers.file_formatter import data_to_dict


def router_monitor(comm, command, quit_ssh, device, _):
    decoder(comm)
    if "E" in device:
        interfaces = []
        intList = routers_ints[f"RTR{device}"]["ints"]
        for i in range(0, 5):
            command("display interface brief | no-more")
            sleep(2)
            value = decoder(comm)
            for interface in intList:
                interfaces.append(int_formatter(value, interface))

        log(
            f'| {"Interface":^25} | {"PHY":^4} | {"Protocol":^8} | {"InUti":^8} | {"OutUti":^8} | {"inErrors":^8} | {"outErrors":^9} |',
            "normal",
        )

        for interface in interfaces:
            color = (
                "fail"
                if interface["PHY"] != "up" or float(interface["InUti"][:-1]) < 8.0
                else "ok"
            )
            log(
                f'| {interface["Interface"]:^25} | {interface["PHY"]:^4} | {interface["Protocol"]:^8} | {interface["InUti"]:^8} | {interface["OutUti"]:^8} | {interface["inErrors"]:^8} | {interface["outErrors"]:^9} |',
                color,
            )
        quit_ssh()

    if "A" in device:
        dhcp = routers_ints[f"RTR{device}"]["pool"]
        sections = []
        for pool in dhcp:
            command(
                f"display ip pool name dhcp_server_{pool} conflict decline | no-more"
            )
            value = decoder(comm)
            regex = check_iter(value, rtr_conflicts["condition"])
            (_, start) = regex[4]
            (end, _) = regex[5]
            summary = data_to_dict(rtr_conflicts["header"], value[start:end])
            sections.append({"pool": pool, "data": summary})
        for section in sections:
            command(f"ip pool dhcp_server_{section['pool']} server")
            for ips in section["data"]:
                command(f"reset conflict-ip-address {ips['IP']}")
                log(
                    f"Conflicto eliminado en la ip {ips['IP']} en el segmento {section['pool']}",
                    "success",
                )
        quit_ssh()
