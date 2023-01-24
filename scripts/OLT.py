from helpers.utils.decoder import decoder
from helpers.utils.printer import inp, log, colorFormatter
from helpers.utils.ssh import ssh
from time import sleep
from scripts.AD import upgradeData
from scripts.BC import existingLookup
from scripts.CPDC import cpdc
from scripts.EC import deleteClient
from scripts.IX import confirmNew
from scripts.MC import modifyClient
from scripts.MG import migration
from scripts.OX import operate
from scripts.VC import verifyTraffic
from scripts.XP import portOperation
from helpers.info.hashMaps import devices


def olt():
    oltOptions = ["1", "2", "3"]
    olt = inp("Seleccione la OLT [1 | 2 | 3] : ").upper()
    if olt in oltOptions:
        ip = devices[f"OLT{olt}"]
        (comm, command, quit) = ssh(ip)
        decoder(comm)

        action = inp(
            """
Que accion se realizara? 
    > (RL)  :   Reactivar con lista
    > (RU)  :   Reactivar uno
    > (SL)  :   Suspender con lista
    > (SU)  :   Suspender uno
    > (IN)  :   Instalar nuevo
    > (IP)  :   Instalar previo
    > (BC)  :   Buscar cliente en OLT
    > (EC)  :   Eliminar Cliente
    > (MC)  :   Modificar Cliente
    > (VC)  :   Verificar consumo
    > (VP)  :   Verificacion de puerto
    > (CA)  :   Clientes con averias (corte de fibra)
    > (DT)  :   Desactivados Totales
    > (MG)  :   Migracion OLT
    > (AD)  :   Actualizacion de datos en olt
    > (DC)  :   CPDC
$ """
        )


        modules = {
            "RL": operate,
            "RU": operate,
            "SL": operate,
            "SU": operate,
            "IN": confirmNew,
            "IP": confirmNew,
            "BC": existingLookup,
            "EC": deleteClient,
            "MC": modifyClient,
            "VC": verifyTraffic,
            "VP": portOperation,
            "CA": portOperation,
            "DT": portOperation,
            "MG": migration,
            "AD": upgradeData,
            "DC": cpdc,
        }

        modules[action](comm, command, quit, olt, action)
    else:
        resp = colorFormatter(
            f"No se puede Conectar a la OLT, Error OLT {olt} no existe", "warning")
        log(resp)
        sleep(1)
