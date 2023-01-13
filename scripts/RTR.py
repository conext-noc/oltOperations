from time import sleep
from helpers.info.hashMaps import devices
from helpers.utils.printer import colorFormatter, inp, log
from helpers.utils.decoder import decoder
from helpers.utils.interfaceHandler import intFormatter
from helpers.utils.ssh import ssh


def rtr():
    rtrTypes = ["e1", "e2", "a1", "a2"]
    ip = ""
    interfaces = []
    rt = inp(
        "Selecciona el router a monitorear [E1 | E2 | A1 | A2] : ")
    if rt in rtrTypes:
        ip = devices[f"RTR{rt}"]["ip"]
        intList = devices[f"RTR{rt}"]["ints"]
        (comm, command, quit) = ssh(ip)
        decoder(comm)
        if "E" in rt:
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
            ""
    else:
        resp = colorFormatter(
            f"No se puede Conectar al router, Error Router {rt} no existe", "warning")
        log(resp)
        sleep(1)
