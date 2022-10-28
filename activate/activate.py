from tkinter import filedialog
from helpers.csvParser import parser
from helpers.listChecker import compare
from helpers.outputDecoder import sshToFile


def activate(comm, command, olt, typeOfList):
    actionList = []
    if typeOfList == "RO":
        print("Selecciona el archivo de lista de clientes de ODOO")
        odoo = filedialog.askopenfilename()
        print("Selecciona el archivo de lista de clientes de Drive")
        drive = filedialog.askopenfilename()
        actionList = compare(parser(odoo), parser(drive), olt)
    elif typeOfList == "RC":
        print("Selecciona la lista de clientes")
        lista = filedialog.askopenfilename()
        actionList = parser(lista)
    elif typeOfList == "RU":
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
            command(f"ont activate {PORT} {ID}")
            command(f"display ont info {PORT} {ID}")
            if typeOfList != "RU":
                path = f"{typeOfList}_{FRAME}-{SLOT}-{PORT}-{ID}_OLT{OLT}.txt"
                sshToFile(comm, path)
        command("quit")
        return actionList
    else:
        print("\nla lista no tiene ningun cliente...\n")
        return
