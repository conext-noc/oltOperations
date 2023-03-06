from time import sleep
from helpers.info.hashMaps import devices
from helpers.utils.printer import colorFormatter, inp, log
from helpers.utils.decoder import checkIter, decoder
from helpers.utils.interfaceHandler import intFormatter
from helpers.utils.ssh import ssh
from helpers.info.regexConditions import rtrConflicts
from helpers.fileFormatters.fileHandler import dataToDict

def rtr():
    rtrTypes = ["E1", "E2", "A1", "A2"]
    rt = inp(
        "Selecciona el router a monitorear [E1 | E2 | A1 | A2] : ")
    debugging = input('Desea debbug los comandos [mostrar comandos]? (y/n): ').lower().strip() == 'y'
    ip = devices[f"RTR{rt}"]["ip"]
    (comm, command, quit) = ssh(ip, debugging)
    if rt in rtrTypes:
        decoder(comm)
        if "E" in rt:
            interfaces = []
            intList = devices[f"RTR{rt}"]["ints"]
            for i in range(0, 5):
                command("display interface brief | no-more")
                value = decoder(comm)
                for interface in intList:
                    interfaces.append(intFormatter(value, interface))

            log(
                "| {:^25} | {:^4} | {:^8} | {:^8} | {:^8} | {:^8} | {:^9} |".format(
                    "Interface", "PHY", "Protocol", "InUti", "OutUti", "inErrors", "outErrors"
                )
            )

            for interface in interfaces:
                color = "fail" if interface["PHY"] != 'up' or float(
                    interface["InUti"][:-1]) < 8.0 else "ok"
                res = colorFormatter("| {:^25} | {:^4} | {:^8} | {:^8} | {:^8} | {:^8} | {:^9} |".format(
                    interface["Interface"], interface["PHY"], interface["Protocol"], interface[
                        "InUti"], interface["OutUti"], interface["inErrors"], interface["outErrors"]
                ), color)
                log(res)
            quit()
        if "A" in rt:
            dhcp = devices[f"RTR{rt}"]["pool"]
            sectionMapper = devices[f"RTR{rt}"]["section"]
            sections = []
            ranges = []
            for pool in dhcp:
                command(f"ip pool dhcp_server_{pool} server")
                command(f"display ip pool name dhcp_server_{pool} conflict decline | no-more")
                value = decoder(comm)
                regex = checkIter(value,rtrConflicts["condition"])
                (_,start) = regex[1]
                (end,_) = regex[2]
                summary = dataToDict(rtrConflicts["headerConf"], value[start:end])
                sections.append({f"{pool}":summary,"value":value, "regex": regex})
            for section, pool in zip(sections,dhcp):
                for idx, st in enumerate(section[pool]):
                    log(colorFormatter(f"En segmento {idx + 1} del pool [{pool}] hay {st['conflict']} conflictos", "info"))
                    if int(st["conflict"]) > 0:
                        (_,start) = section["regex"][sectionMapper[str(idx + 1)]["start"]]
                        (end,_) = section["regex"][sectionMapper[str(idx + 1)]["end"]]
                        data = dataToDict(rtrConflicts["headerSect"], section["value"][start:end])
                        ranges.append({"data":data, "pool": pool})
            for rg in ranges:
                command(f"ip pool dhcp_server_{rg['pool']} server")
                for address in rg["data"]:
                    command(f"reset conflict-ip-address {address['ip']}")
                    log(colorFormatter(f"Conflicto eliminado en la ip {address['ip']}", "success"))
            quit()
    else:
        resp = colorFormatter(
            f"No se puede Conectar al router, Error Router {rt} no existe", "warning")
        log(resp)
        sleep(1)