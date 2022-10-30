from tkinter import filedialog
from helpers.csvParser import parserCSV
from helpers.formatter import colorFormatter
from helpers.listChecker import compare
from helpers.outputDecoder import sshToFile


def deactivate(comm, command, olt, typeOfList):
    actionList = []
    if typeOfList == "SO":
        print("Selecciona el archivo de lista de clientes de ODOO")
        odoo = filedialog.askopenfilename()
        print("Selecciona el archivo de lista de clientes de Drive")
        drive = filedialog.askopenfilename()
        actionList = compare(parserCSV(odoo), parserCSV(drive), olt)
    elif typeOfList == "SC":
        print("Selecciona la lista de clientes")
        lista = filedialog.askopenfilename()
        actionList = parserCSV(lista)
    elif typeOfList == "SU":
        NAME = input("Ingrese nombre del cliente : ").upper()
        SLOT = input("Ingrese slot de cliente : ").upper()
        PORT = input("Ingrese puerto de cliente : ").upper()
        ID = input("Ingrese el id del cliente : ").upper()
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
        resp = '\nNingun tipo de lista se ha seleccionado, tip: respuestas posibles "Y" para listas con datos de ODOO y "N" para listas sin datos de ODOO\n'
        resp = colorFormatter(resp,"warning")
        print(resp)
        return
    if len(actionList) > 0:
        for client in actionList:
            NAME = client["NOMBRE"]
            OLT = client["OLT"]
            FRAME = client["FRAME"]
            SLOT = client["SLOT"]
            PORT = client["PORT"]
            ID = client["ID"]
            resp = f"{NAME} @ OLT {OLT} IN {FRAME}/{SLOT}/{PORT}/{ID}"
            resp = colorFormatter(resp,"success")
            print(resp)
            command(f"interface gpon {FRAME}/{SLOT}")
            command(f"ont deactivate {PORT} {ID}")
            command(f"display ont info {PORT} {ID}")
            if typeOfList != "SU":
                path = f"{typeOfList}_{FRAME}-{SLOT}-{PORT}-{ID}_OLT{OLT}.txt"
                sshToFile(comm, path)
        command("quit")
        return actionList
    else:
        resp = "\nla lista no tiene ningun cliente...\n"
        resp = colorFormatter(resp,"warning")
        print(resp)
        return
