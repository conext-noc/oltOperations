import os
import tkinter as tk
from dotenv import load_dotenv
from helpers.verification import verify
from deactivate.deactivate import deactivate
from activate.activate import activate
from delete.delete import delete
from confirm.confirm import confirm
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

def operations(action,comm,enter,command,OLT):
  try:
    option = {
      "AA": activate(comm,enter,command,OLT),
      "AO": activate(comm,enter,command,OLT),
      "CC": deactivate(comm,enter,command,OLT),
      "CO": deactivate(comm,enter,command,OLT),
      "IN": confirm(comm,enter,command,OLT,"IN"),
      "IP": confirm(comm,enter,command,OLT,"IP"),
      "EE": delete(comm,command,enter, OLT),
      "CP": "fun2()",
      "CE": "fun2()",
      "VV": "fun2()",
      "VC": "fun2()",
      "VR": "fun2()",
      "PC": "fun2()",
      }
    return option[action]
  except KeyError:
    raise Exception(f"Error @ : opcion {action} no existe")

def main():
  delay = 1
  while True:
    try:
      olt = input("en cual olt se realizara? [15|2] : ")
      ip = ""
      if(olt == "15"):
        ip = "181.232.180.5" 
      elif (olt == "2"):
        ip = "181.232.180.6"
      else:
        raise Exception("Cannot connect to olt")

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

      action = input("""
    Que accion se realizara? 
      > (AA)  :  activar
      > (AO)  :  activar con datos de odoo
      > (CC)  :  corte
      > (CO)  :  corte con datos de odoo
      > (IN)  :  instalar nuevo
      > (IP)  :  confirmar ya preinstalado
      > (EE)  :  eliminar cliente
      > (CP)  :  cambio de plan
      > (CE)  :  cambio de ont
      > (VV)  :  verificar valores de ont
      > (VC)  :  verificar consumo
      > (VR)  :  verificar reset
      > (PC)  :  cambio proveedor
    $ """)

      # TURN THIS TO A HASH MAP
      if(action == "AA"):
        result = activate(comm,enter,command,olt)
        verify(result,action,olt)
      elif(action == "AO"):
        result = activate(comm,enter,command,olt)
        verify(result,action,olt)
      elif(action == "CC"):
        result = deactivate(comm,enter,command,olt)
        verify(result,action,olt)
      elif(action == "CO"):
        result = deactivate(comm,enter,command,olt)
        verify(result,action,olt)
      elif(action == "IN"):
        confirm(comm,enter,command,olt,"IN")
      elif(action == "IP"):
        confirm(comm,enter,command,olt,"IP")
      elif(action == "EE"):
        delete(comm,command,enter, olt)
      elif(action == "CP"):
        ""
      elif(action == "CE"):
        ""
      elif(action == "VV"):
        ""
      elif(action == "VC"):
        ""
      elif(action == "VR"):
        ""
      elif(action == "PC"):
        ""
      else:
        print(f"Error @ : opcion {action} no existe")
      conn.close()

    except Exception:
      print("Error At : ", traceback.format_exc())
    except KeyboardInterrupt:
      print("Saliendo...")
      sys.exit(0)


if __name__ == "__main__":
  main()