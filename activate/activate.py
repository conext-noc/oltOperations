from tkinter import filedialog
from helpers.csvParser import parser
from helpers.listChecker import compare

class NoListSelected(Exception):
  """Ningun tipo de lista se ha seleccionado, tip: respuestas posibles "Y" para listas con datos de ODOO y "N" para listas sin datos de ODOO"""
  pass

class NoClientsInList(Exception):
  """la lista no tiene ningun cliente..."""
  pass

def activate(comm,enter,command,olt,typeOfList):
    actionList = []
    if(typeOfList == "AO"):
        print("Selecciona el archivo de lista de clientes de ODOO")
        odoo = filedialog.askopenfilename()
        print("Selecciona el archivo de lista de clientes de Drive")
        drive = filedialog.askopenfilename()
        actionList = compare(parser(odoo),parser(drive), olt)

    elif(typeOfList == "AA"):
        print("Selecciona la lista de clientes")
        lista = filedialog.askopenfilename()
        actionList = parser(lista)

    elif(typeOfList == "AI"):
        NAME = input("Ingrese nombre del cliente : ")
        SLOT = input("Ingrese slot de cliente : ")
        PORT = input("Ingrese puerto de cliente : ")
        ID = input("Ingrese el id del cliente : ")
        actionList=[{"NOMBRE":NAME,"OLT":olt,"FRAME":0,"SLOT":SLOT,"PORT":PORT,"ID":ID}]
    else:
        raise NoListSelected
    if(len(actionList) > 0):
        for client in actionList:
            print(client["NOMBRE"], client["OLT"],client["FRAME"],client["SLOT"],client["PORT"],client["ID"])
            command(
                "interface gpon {}/{}".format(client["FRAME"], client["SLOT"]))
            enter()
            command("ont activate {} {}".format(
                client["PORT"], client["ID"]))
            enter()
            command("display ont info {} {} | include \"Control flag\" ".format(
                client["PORT"], client["ID"]))
            enter()
            command("quit")
            enter()
            outputClient = comm.recv(65535)
            outputClient = outputClient.decode("ascii")
            OLT = client["OLT"]
            FRAME = client["FRAME"] if (client["FRAME"] != "N/A" and client["FRAME"] != "") else "NA"
            SLOT = client["SLOT"] if (client["SLOT"] != "N/A" and client["SLOT"] != "") else "NA"
            PORT = client["PORT"] if (client["PORT"] != "N/A" and client["PORT"] != "") else "NA"
            clientID = client["ID"] if (client["ID"] != "N/A" and client["ID"] != "") else "NA"
            path = f"{typeOfList}_{FRAME}-{SLOT}-{PORT}-{clientID}_OLT{OLT}.txt"
            print(outputClient, file=open(path, "w"))
        return actionList
    else:
        raise NoClientsInList
