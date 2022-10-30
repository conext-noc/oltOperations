import tkinter as tk
from helpers.ssh import ssh
from helpers.outputDecoder import decoder
from helpers.verification import verify
from SX.deactivate import deactivate
from RX.activate import activate
from EC.delete import delete
from IX.confirm import confirm
from MC.deviceModify import deviceModify
from VC.speedVerify import speedVerify
from VR.verifyReset import verifyReset
from VP.verifyPort import verifyPort
from BX.lookup import existingLookup, newLookup
from CA.clientFault import clientFault
import traceback
import sys

root = tk.Tk()
root.withdraw()


def main():
    while True:
        try:
            olt = input("Seleccione la OLT [15|2] : ")
            ip = ""
            if olt == "15":
                ip = "181.232.180.5"
            elif olt == "2":
                ip = "181.232.180.6"
            else:
                raise Exception(
                    f"No se puede Conectar a la OLT, Error OLT {olt} no existe"
                )

            (comm, command) = ssh(ip)

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
                result = activate(comm, command, olt, action)
                verify(result, action, olt)
            elif action == "RO":
                result = activate(comm, command, olt, action)
                verify(result, action, olt)
            elif action == "RU":
                result = activate(comm, command, olt, action)
            elif action == "SC":
                result = deactivate(comm, command, olt, action)
                verify(result, action, olt)
            elif action == "SO":
                result = deactivate(comm, command, olt, action)
                verify(result, action, olt)
            elif action == "SU":
                result = deactivate(comm, command, olt, action)
            elif action == "IN":
                confirm(comm, command, olt, action)
            elif action == "IP":
                confirm(comm, command, olt, action)
            elif action == "EC":
                delete(comm, command, olt)
            elif action == "BN":
                newLookup(comm, command, olt)
            elif action == "BE":
                existingLookup(comm, command, olt)
            elif action == "MC":
                deviceModify(comm, command, olt)
            elif action == "VC":
                speedVerify(comm, command)
            elif action == "VR":
                verifyReset(comm, command)
            elif action == "VP":
                verifyPort(comm, command)
            elif action == "CA":
                clientFault(comm, command, olt)
            else:
                print(f"Error @ : opcion {action} no existe")

        except KeyboardInterrupt:
            print("Saliendo...")
            sys.exit(0)
        except Exception:
            print("Error At : ", traceback.format_exc())


if __name__ == "__main__":
    main()
