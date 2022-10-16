from tkinter import filedialog
from helpers.csvParser import parser
from helpers.listChecker import compare
from helpers.outputDecoder import sshToFile


def deactivate(comm, enter, command, olt, typeOfList):
    actionList = []
    if typeOfList == "SO":
        print("Selecciona el archivo de lista de clientes de ODOO")
        odoo = filedialog.askopenfilename()
        print("Selecciona el archivo de lista de clientes de Drive")
        drive = filedialog.askopenfilename()
        actionList = compare(parser(odoo), parser(drive), olt)
    elif typeOfList == "SC":
        print("Selecciona la lista de clientes")
        lista = filedialog.askopenfilename()
        actionList = parser(lista)
    elif typeOfList == "SU":
        NAME = input("Ingrese nombre del cliente : ")
        SLOT = input("Ingrese slot de cliente : ")
        PORT = input("Ingrese puerto de cliente : ")
        ID = input("Ingrese el id del cliente : ")
        actionList = [
            {
                "NOMBRE": NAME,
                "OLT": olt,
                "FRAME": 0,
                "SLOT": SLOT,
                "PORT": PORT,
                "ID": ID,
            }
        ]
    else:
        print(
            '\nNingun tipo de lista se ha seleccionado, tip: respuestas posibles "Y" para listas con datos de ODOO y "N" para listas sin datos de ODOO\n'
        )
        return
    if len(actionList) > 0:
        for client in actionList:
            NAME = client["NOMBRE"]
            OLT = client["OLT"]
            FRAME = client["FRAME"]
            SLOT = client["SLOT"]
            PORT = client["PORT"]
            ID = client["ID"]
            print(f"{NAME} @ OLT {OLT} IN {FRAME}/{SLOT}/{PORT}/{ID}")
            command(f"interface gpon {FRAME}/{SLOT}")
            enter()
            command(f"ont deactivate {PORT} {ID}")
            enter()
            command(f'display ont info {PORT} {ID} | include "Control flag" ')
            enter()
            if typeOfList != "SU":
                path = f"{typeOfList}_{FRAME}-{SLOT}-{PORT}-{ID}_OLT{OLT}.txt"
                sshToFile(comm, path)
        command("quit")
        enter()
        return actionList
    else:
        print("\nla lista no tiene ningun cliente...\n")
        return
