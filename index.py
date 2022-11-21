import tkinter as tk
from time import sleep
from helpers.ssh import ssh
from helpers.outputDecoder import decoder
from helpers.verification import verify
from scripts.SX import deactivate
from scripts.RX import activate
from scripts.EC import delete
from scripts.IX import confirm
from scripts.MC import deviceModify
from scripts.VC import speedVerify
from scripts.VR import verifyReset
from scripts.VP import verifyPort
from scripts.BX import existingLookup, newLookup
from scripts.CA import clientFault
import traceback
import sys
from helpers.formatter import colorFormatter

root = tk.Tk()
root.withdraw()


def main():
    try:
        while True:
            olt = input("Seleccione la OLT [15|2] : ").upper()
            if olt == "15" or olt == "2":
                ip = "181.232.180.5" if olt == "15" else "181.232.180.6"
                (comm, command, close) = ssh(ip)
                def quit(delay):
                    close()
                    sleep(delay)
                    sys.exit(0)

                command("enable")
                command("config")
                decoder(comm)

                action = input(
                    """
    Que accion se realizara? 
        > (RC)  :  Reactivar Clientes (lista)
        > (RO)  :  Reactivar con lista de Odoo
        > (RU)  :  Reactivar uno
        > (SC)  :  Suspender Clientes
        > (SO)  :  Suspender con lista de Odoo
        > (SU)  :  Suspender uno
        > (IN)  :  Instalar nuevo
        > (IP)  :  Instalar previo
        > (EC)  :  Eliminar Cliente
        > (BN)  :  Buscar cliente en OLT (no agregado)
        > (BE)  :  Buscar cliente en OLT (ya agregado)
        > (MC)  :  Modificar Cliente
        > (VC)  :  Verificar consumo
        > (VR)  :  Verificar reset
        > (VP)  :  Verificacion de puerto
        > (CA)  :  Clientes con averias (corte de fibra)
    $ """
                ).upper()

                if action == "RC":
                    result = activate(comm, command, olt, action, quit)
                    verify(result, action, olt, quit)
                elif action == "RO":
                    result = activate(comm, command, olt, action, quit)
                    verify(result, action, olt, quit)
                elif action == "RU":
                    result = activate(comm, command, olt, action, quit)
                elif action == "SC":
                    result = deactivate(comm, command, olt, action, quit)
                    verify(result, action, olt, quit)
                elif action == "SO":
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
                elif action == "BN":
                    newLookup(comm, command, olt, quit)
                elif action == "BE":
                    existingLookup(comm, command, olt, quit)
                elif action == "MC":
                    deviceModify(comm, command, olt, quit)
                elif action == "VC":
                    speedVerify(comm, command, quit)
                elif action == "VR":
                    verifyReset(comm, command, quit)
                elif action == "VP":
                    verifyPort(comm, command)
                    quit(10)
                elif action == "CA":
                    clientFault(comm, command, olt)
                    quit(180)
                else:
                    resp = colorFormatter(f"Error @ : opcion {action} no existe", "warning")
                    print(resp)
                    quit(2)
            else:
                resp = colorFormatter(f"No se puede Conectar a la OLT, Error OLT {olt} no existe", "warning")
                print(resp)
                sleep(1)
                sys.exit(0)
    except KeyboardInterrupt:
        resp = colorFormatter("Saliendo...", "warning")
        print(resp)
        sleep(0.5)
        sys.exit(0)
    except Exception:
        resp = colorFormatter(f"Error At : {traceback.format_exc()}", "fail")
        print(resp)
        sleep(10)
        sys.exit(1)


if __name__ == "__main__":
    main()
