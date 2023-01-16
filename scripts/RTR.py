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
    ip = devices[f"RTR{rt}"]["ip"]
    (comm, command, quit) = ssh(ip)
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
            pool = devices[f"RTR{rt}"]["pool"]
            sectionMapper = devices[f"RTR{rt}"]["section"]
            sections = []
            ranges = []
            ipAddressess = []
            command("sys")
            command(f"ip pool dhcp_server_residencial_{pool} server")
            command(f"display ip pool name dhcp_server_residencial_{pool} conflict decline | no-more")
            value = decoder(comm)
            regex = checkIter(value,rtrConflicts["condition"])
            (_,start) = regex[1]
            (end,_) = regex[2]
            summary = dataToDict(rtrConflicts["headerConf"], value[start:end])
            for idx, section in enumerate(summary):
                log(colorFormatter(f"En segmento {idx + 1} hay {section['conflict']} conflictos", "info"))
                if int(section["conflict"]) > 0:
                    sections.append(sectionMapper[str(idx + 1)])
            for section in sections:
                (_,start) = regex[section["start"]]
                (end,_) = regex[section["end"]]
                data = dataToDict(rtrConflicts["headerSect"], value[start:end])
                ranges.append(data)
            for rg in ranges:
                for ipAddStatus in rg:
                    ipAddressess.append(ipAddStatus["ip"])
                    
            for ip in ipAddressess:
                command(f"reset conflict-ip-address {ip}")
                log(colorFormatter(f"Conflicto eliminado en la ip {ip}", "success"))
            quit()
    else:
        resp = colorFormatter(
            f"No se puede Conectar al router, Error Router {rt} no existe", "warning")
        log(resp)
        sleep(1)
