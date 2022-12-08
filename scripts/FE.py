import gspread
from helpers.printer import inp
from scripts.CL import listCompare
from scripts.PL import planChanger
from scripts.CPDC import cpdc


def utils(comm,command,quit,olt):
    sa = gspread.service_account(
        filename="service_account_olt_operations.json")
    sh = sa.open("CPDC")
    wks = sh.worksheet("DATOS")
    action = inp(
        """
Que accion se realizara? 
  > (CL)    :   Comparar Listas
  > (PL)    :   Cambio de Plan (lista)
  > (CPDC)  :   Ejecutar lista Clientes por Plan De Consumo
$ """
    ).upper()
    
    if action == "CL":
      listCompare()
    elif action == "PL":
      planChanger(comm, command, quit, olt)
    elif action == "CPDC":
      cpdc(comm, command, olt,quit)
