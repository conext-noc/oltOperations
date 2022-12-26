from helpers.utils.decoder import decoder
from helpers.utils.printer import inp, log, colorFormatter
from helpers.utils.ssh import ssh
from time import sleep
from scripts.AD import upgradeData
from scripts.BC import existingLookup
from scripts.EC import deleteClient
from scripts.IX import confirm
from scripts.IXN import confirmNew
from scripts.MC import modifyClient
from scripts.MG1 import migration
from scripts.MG2 import addWanConfig

from scripts.OX import operate
from scripts.VC import verifyTraffic
from scripts.XP import portOperation


def olt():
    oltOptions = ["1", "2", "3"]
    olt = inp("Seleccione la OLT [1 | 2 | 3] : ").upper()
    if olt in oltOptions:
        ip = "181.232.180.7" if olt == "1" else "181.232.180.5" if olt == "2" else "181.232.180.6"
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
$ """
        )
        if action == "RL":
            operate(comm,command,quit,olt,action)
        if action == "RU":
            operate(comm,command,quit,olt,action)
        if action == "SL":
            operate(comm,command,quit,olt,action)
        if action == "SU":
            operate(comm,command,quit,olt,action)
        if action == "IN":
            confirm(comm,command,quit,olt,action) if olt != "1" else confirmNew(comm,command,quit,olt,action)
        if action == "IP":
            confirm(comm,command,quit,olt,action) if olt != "1" else confirmNew(comm,command,quit,olt,action)
        if action == "BC":
            existingLookup(comm,command,quit,olt)
        if action == "EC":
            deleteClient(comm,command,quit,olt)
        if action == "MC":
            modifyClient(comm,command,quit,olt)
        if action == "VC":
            verifyTraffic(comm,command,quit,olt)
        if action == "VP":
            portOperation(comm,command,quit,olt,action)
        if action == "CA":
            portOperation(comm,command,quit,olt,action)
        if action == "DT":
            portOperation(comm,command,quit,olt,action)
        if action == "MG":
            stage = inp("Que etapa de migracion desea utilizar [1 | 2] : ")
            migration(comm,command,quit,olt) if stage == "1" else addWanConfig(comm,command,quit,olt) if stage == "2" else None
        if action == "AD":
            upgradeData(comm, command, quit, olt)
    else:
        resp = colorFormatter(
            f"No se puede Conectar a la OLT, Error OLT {olt} no existe", "warning")
        log(resp)
        sleep(1)
