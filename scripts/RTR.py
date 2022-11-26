from time import sleep
from helpers.printer import inp, log, colorFormatter
from helpers.ssh import ssh
from helpers.outputDecoder import decoder
from helpers.interfaceData import intFormatter

intfacesC1 = ["GigabitEthernet0/3/7(10G)"]
intfacesC2 = ["GigabitEthernet0/3/7(10G)", "GigabitEthernet0/3/8(10G)"]


def rtr():
    ip = ""
    interfaces = []
    rt = inp(
        "Selecciona el router de borde a monitorear [INTER | VNET] : ").upper()
    if rt == "INTER" or rt == "VNET":
        ip = "181.232.180.1" if rt == "INTER" else "181.232.180.2"
        intList = intfacesC1 if rt == "INTER" else intfacesC2
        (comm, command, quit) = ssh(ip)
        decoder(comm)
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
            color = "fail" if interface["PHY"] != 'up' or interface["Protocol"] != 'up'or float(interface["InUti"][:-1]) < 8.0 else "ok"
            res = colorFormatter("| {:^25} | {:^4} | {:^8} | {:^8} | {:^8} | {:^8} | {:^9} |".format(
                interface["Interface"], interface["PHY"], interface["Protocol"], interface[
                    "InUti"], interface["OutUti"], interface["inErrors"], interface["outErrors"]
            ), color)
            log(res)
        quit()

    else:
        resp = colorFormatter(
            f"No se puede Conectar al router de borde, Error Router {rt} no existe", "warning")
        log(resp)
        sleep(1)
