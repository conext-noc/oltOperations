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
            print(i)
            command("display interface brief | no-more")
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
        dhcp = routers_ints[f"deviceR{device}"]["pool"]
        section_mapper = routers_ints[f"RTR{device}"]["section"]
        sections = []
        ranges = []
        for pool in dhcp:
            command(f"ip pool dhcp_server_{pool} server")
            command(
                f"display ip pool name dhcp_server_{pool} conflict decline | no-more"
            )
            value = decoder(comm)
            regex = check_iter(value, rtr_conflicts["condition"])
            (_, start) = regex[1]
            (end, _) = regex[2]
            summary = data_to_dict(rtr_conflicts["headerConf"], value[start:end])
            sections.append({f"{pool}": summary, "value": value, "regex": regex})
        for section, pool in zip(sections, dhcp):
            for idx, st in enumerate(section[pool]):
                log(
                    f"En segmento {idx + 1} del pool [{pool}] hay {st['conflict']} conflictos",
                    "info",
                )
                if int(st["conflict"]) > 0:
                    (_, start) = section["regex"][section_mapper[str(idx + 1)]["start"]]
                    (end, _) = section["regex"][section_mapper[str(idx + 1)]["end"]]
                    data = data_to_dict(
                        rtr_conflicts["headerSect"], section["value"][start:end]
                    )
                    ranges.append({"data": data, "pool": pool})
        for rg in ranges:
            command(f"ip pool dhcp_server_{rg['pool']} server")
            for address in rg["data"]:
                command(f"reset conflict-ip-address {address['ip']}")
                log(f"Conflicto eliminado en la ip {address['ip']}", "success")
        quit_ssh()
