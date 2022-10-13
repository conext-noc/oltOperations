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
from deviceChange.deviceChange import deviceChange
from valueVerify.valueVerify import valueVerify
from speedVerify.speedVerify import speedVerify
from verifyReset.verifyReset import verifyReset
from verifyPort.verifyPort import verifyPort
from ontLookup.lookup import existingLookup,newLookup
from providerChange.providerChange import providerChange
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


class NoListSelected(Exception):
    """Ningun tipo de lista se ha seleccionado, tip: respuestas posibles "Y" para listas con datos de ODOO y "N" para listas sin datos de ODOO"""
    pass


class NoClientsInList(Exception):
    """la lista no tiene ningun cliente..."""
    pass


def main():
    delay = 1
    while True:
        try:
            olt = input("Seleccione la OLT [15|2] : ")
            ip = ""
            if (olt == "15"):
                ip = "181.232.180.5"
            elif (olt == "2"):
                ip = "181.232.180.6"
            else:
                raise Exception(
                    f"No se puede Conectar a la OLT, Error OLT {olt} no existe")

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

            action = input("""
Que accion se realizara? 
  > (AA)  :  Activar
  > (AO)  :  Activar con datos de odoo
  > (AI)  :  Activar cliente (1)
  > (CC)  :  Corte
  > (CO)  :  Corte con datos de odoo
  > (CI)  :  Cortar cliente (1)
  > (IN)  :  Instalar nuevo
  > (IP)  :  Instalar previo
  > (EE)  :  Eliminar cliente
  > (BN)  :  Buscar cliente en OLT (no agregado)
  > (BC)  :  Buscar cliente en OLT (ya agregado)
  > (CP)  :  Cambio de plan
  > (CE)  :  Cambio de equipo
  > (VV)  :  Verificar valores de ont
  > (VC)  :  Verificar consumo
  > (VR)  :  Verificar reset
  > (VS)  :  Verificar Service-Port ID
  > (VP)  :  Verificacion de puerto
  > (CV)  :  Cambio Vlan (Proveedor)
$ """)

            # TURN THIS TO A HASH MAP
            if (action == "AA"):
                result = activate(comm, enter, command, olt, action)
                verify(result, action, olt)
            elif (action == "AO"):
                result = activate(comm, enter, command, olt, action)
                verify(result, action, olt)
            elif (action == "AI"):
                result = activate(comm, enter, command, olt, action)
            elif (action == "CC"):
                result = deactivate(comm, enter, command, olt, action)
                verify(result, action, olt)
            elif (action == "CO"):
                result = deactivate(comm, enter, command, olt, action)
                verify(result, action, olt)
            elif (action == "CI"):
                result = deactivate(comm, enter, command, olt, action)
            elif (action == "IN"):
                confirm(comm, enter, command, olt, action)
            elif (action == "IP"):
                confirm(comm, enter, command, olt, action)
            elif (action == "EE"):
                delete(comm, command, enter, olt)
            elif (action == "BN"):
                newLookup(comm, command, enter, olt)
            elif (action == "BC"):
                existingLookup(comm, command, enter, olt)
            elif (action == "CP"):
                newPlan(comm, command, enter, olt)
            elif (action == "CE"):
                deviceChange(comm, command, enter, olt)
            elif (action == "VV"):
                valueVerify(comm, command, enter)
            elif (action == "VC"):
                speedVerify(comm, command, enter)
            elif (action == "VR"):
                verifyReset(comm, command, enter)
            elif (action == "VP"):
                verifyPort(comm, command, enter)
            elif (action == "VS"):
                spid = input("Ingrese el Service-Port ID : ")
                verifySPID(comm, command, enter,spid)
            elif (action == "CV"):
                providerChange(comm, command, enter,olt)
            else:
                print(f"Error @ : opcion {action} no existe")
            conn.close()

        except Exception:
            print("Error At : ", traceback.format_exc())
        except NoListSelected(Exception):
            print("""Ningun tipo de lista se ha seleccionado, tip: respuestas posibles "Y" para listas con datos de ODOO y "N" para listas sin datos de ODOO""")
        except NoClientsInList(Exception):
            print("la lista no tiene ningun cliente...")
        except KeyboardInterrupt:
            print("Saliendo...")
            sys.exit(0)


if __name__ == "__main__":
    main()
