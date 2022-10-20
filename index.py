import os
import tkinter as tk
from dotenv import load_dotenv
from helpers.spidInfo import verifySPID
from helpers.verification import verify
from deactivate.deactivate import deactivate
from activate.activate import activate
from delete.delete import delete
from confirm.confirm import confirm
from planMigration.planMigration import newPlan
from deviceChange.deviceModify import deviceModify
from valueVerify.valueVerify import valueVerify
from speedVerify.speedVerify import speedVerify
from verifyReset.verifyReset import verifyReset
from verifyPort.verifyPort import verifyPort
from ontLookup.lookup import existingLookup, newLookup
from providerChange.providerChange import providerChange
from clientFault.clientFault import clientFault
import paramiko
import time
import traceback
import sys

load_dotenv()

username = os.environ["user"]
password = os.environ["password"]
port = os.environ["port"]
root = tk.Tk()
root.withdraw()


def main():
    delay = 1
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

            conn = paramiko.SSHClient()
            conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            conn.connect(ip, port, username, password)
            comm = conn.invoke_shell()

            def enter():
                comm.send(" \n")
                comm.send(" \n")
                time.sleep(delay)

            def command(cmd):
                comm.send(cmd)
                time.sleep(delay)

            command("enable")
            enter()
            command("config")
            enter()
            output = comm.recv(65535)
            output = output.decode("ascii")

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
  > (CP)  :  Cambio de plan
  > (MC)  :  Modificar Cliente
  > (VV)  :  Verificar valores de ont
  > (VC)  :  Verificar consumo
  > (VR)  :  Verificar reset
  > (VS)  :  Verificar Service-Port ID
  > (VP)  :  Verificacion de puerto
  > (CV)  :  Cambio Vlan (Proveedor)
  > (CA)  :  Clientes con averias (corte de fibra)
$ """
            )

            if action == "RC":
                result = activate(comm, enter, command, olt, action)
                verify(result, action, olt)
            elif action == "RO":
                result = activate(comm, enter, command, olt, action)
                verify(result, action, olt)
            elif action == "RU":
                result = activate(comm, enter, command, olt, action)
            elif action == "SC":
                result = deactivate(comm, enter, command, olt, action)
                verify(result, action, olt)
            elif action == "SO":
                result = deactivate(comm, enter, command, olt, action)
                verify(result, action, olt)
            elif action == "SU":
                result = deactivate(comm, enter, command, olt, action)
            elif action == "IN":
                confirm(comm, enter, command, olt, action)
            elif action == "IP":
                confirm(comm, enter, command, olt, action)
            elif action == "EC":
                delete(comm, command, enter, olt)
            elif action == "BN":
                newLookup(comm, command, enter, olt)
            elif action == "BE":
                existingLookup(comm, command, enter, olt)
            elif action == "CP":
                newPlan(comm, command, enter, olt)
            elif action == "MC":
                deviceModify(comm, command, enter, olt)
            elif action == "VV":
                valueVerify(comm, command, enter)
            elif action == "VC":
                speedVerify(comm, command, enter)
            elif action == "VR":
                verifyReset(comm, command, enter)
            elif action == "VP":
                verifyPort(comm, command, enter)
            elif action == "VS":
                spid = input("Ingrese el Service-Port ID : ")
                verifySPID(comm, command, enter, spid)
            elif action == "CV":
                providerChange(comm, command, enter, olt)
            elif action == "CA":
                clientFault(comm, command, enter, olt)
            else:
                print(f"Error @ : opcion {action} no existe")
            conn.close()

        except KeyboardInterrupt:
            print("Saliendo...")
            sys.exit(0)
        except Exception:
            print("Error At : ", traceback.format_exc())
            sys.exit(0)


if __name__ == "__main__":
    main()
