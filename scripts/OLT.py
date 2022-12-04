from helpers.printer import inp, log, colorFormatter
from helpers.outputDecoder import decoder
from helpers.ssh import ssh
from helpers.verification import verify
from scripts.BC import existingLookup
from scripts.CA import clientFault
from scripts.DT import totalDeacts
from scripts.EC import delete
from scripts.IX import confirm
from scripts.MC import deviceModify
from scripts.RX import activate
from scripts.SX import deactivate
from scripts.VC import speedVerify
from scripts.VP import verifyPort
from scripts.VR import verifyReset
from time import sleep


def olt():
    olt = inp("Seleccione la OLT [15|2] : ").upper()
    if olt == "15" or olt == "2":
        ip = "181.232.180.5" if olt == "15" else "181.232.180.6"
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
    > (EC)  :   Eliminar Cliente
    > (BC)  :   Buscar cliente en OLT
    > (MC)  :   Modificar Cliente
    > (VC)  :   Verificar consumo
    > (VR)  :   Verificar reset
    > (VP)  :   Verificacion de puerto
    > (CA)  :   Clientes con averias (corte de fibra)
    > (DT)  :   Desactivados Totales
$ """
        ).upper()

        if action == "RL":
            result = activate(comm, command, olt, action, quit)
            verify(result, action, olt, quit)
        elif action == "RU":
            result = activate(comm, command, olt, action, quit)
        elif action == "SL":
            result = deactivate(comm, command, olt, action, quit)
            verify(result, action, olt, quit)
        elif action == "SU":
            result = deactivate(comm, command, olt, action, quit)
        elif action == "IN":
            confirm(comm, command, olt, action, quit)
        elif action == "IP":
            confirm(comm, command, olt, action, quit)
        elif action == "EC":
            delete(comm, command, olt, quit)
        elif action == "BC":
            existingLookup(comm, command, olt, quit)
        elif action == "MC":
            deviceModify(comm, command, olt, quit)
        elif action == "VC":
            speedVerify(comm, command, quit)
        elif action == "VR":
            verifyReset(comm, command, olt, quit)
        elif action == "VP":
            verifyPort(comm, command)
            quit()
        elif action == "CA":
            clientFault(comm, command, olt)
            quit()
        elif action == "DT":
            totalDeacts(comm, command, olt, quit)
        else:
            resp = colorFormatter(
                f"Error @ : opcion {action} no existe", "warning")
            log(resp)
            quit()
    else:
        resp = colorFormatter(
            f"No se puede Conectar a la OLT, Error OLT {olt} no existe", "warning")
        log(resp)
        sleep(1)
