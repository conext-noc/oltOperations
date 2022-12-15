from helpers.printer import inp, log, colorFormatter
from helpers.outputDecoder import decoder
from helpers.ssh import ssh
from helpers.verification import verify
from scripts.BC import existingLookup
from scripts.CA import clientFault
from scripts.DT import totalDeacts
from scripts.EC import delete
from scripts.IX import confirm
from scripts.IXN import confirmNew
from scripts.MC import deviceModify
from scripts.OX import operate
from scripts.VC import speedVerify
from scripts.VP import verifyPort
from scripts.VR import verifyReset
from time import sleep
from scripts.FE import utils


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
    > (EC)  :   Eliminar Cliente
    > (BC)  :   Buscar cliente en OLT
    > (MC)  :   Modificar Cliente
    > (VC)  :   Verificar consumo
    > (VR)  :   Verificar reset
    > (VP)  :   Verificacion de puerto
    > (CA)  :   Clientes con averias (corte de fibra)
    > (DT)  :   Desactivados Totales
    > (FE)  :   Funciones Extras
$ """
        ).upper()

        if action == "RL":
            result = operate(comm, command, olt, action, quit)
            verify(result, action, olt, quit)
        elif action == "RU":
            result = operate(comm, command, olt, action, quit)
        elif action == "SL":
            result = operate(comm, command, olt, action, quit)
            verify(result, action, olt, quit)
        elif action == "SU":
            result = operate(comm, command, olt, action, quit)
        elif action == "IN":
            if olt == "1":
                confirmNew(comm, command, olt, action, quit)
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
        elif action == "FE":
            utils(comm, command, quit, olt)
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
