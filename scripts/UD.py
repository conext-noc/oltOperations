import gspread
from helpers.printer import inp
from scripts.CL import listCompare


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
$ """
    ).upper()
    
    if action == "CL":
      listCompare()
