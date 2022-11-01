from time import sleep
from tkinter import filedialog
from helpers.csvParser import parserCSV
from helpers.failHandler import failChecker
from helpers.formatter import colorFormatter
from helpers.listChecker import compare
from helpers.outputDecoder import check, decoder, sshToFile
from helpers.serialLookup import serialSearch

existingCond = (
    "-----------------------------------------------------------------------------"
)


def deactivate(comm, command, olt, typeOfList):
    actionList = []
    keep = ""
    if typeOfList == "SO":
        print("Selecciona el archivo de lista de clientes de ODOO")
        odoo = filedialog.askopenfilename()
        print("Selecciona el archivo de lista de clientes de Drive")
        drive = filedialog.askopenfilename()
        actionList = compare(parserCSV(odoo), parserCSV(drive), olt)
        keep = "Y"
    elif typeOfList == "SC":
        print("Selecciona la lista de clientes")
        lista = filedialog.askopenfilename()
        actionList = parserCSV(lista)
        keep = "Y"
    elif typeOfList == "SU":
        lookupType = input(
            "Buscar cliente por serial o por Datos de OLT (F/S/P/ID) [S | D] : "
        ).upper()
        if lookupType == "S":
            SN = input("Ingrese el Serial del Cliente a buscar : ").upper()
            (FRAME, SLOT, PORT, ID, NAME, STATE, fail) = serialSearch(comm, command, SN)
            if fail == None:
                keep = input(
                    f"""
    NOMBRE              :   {NAME}
    OLT                 :   {olt}
    FRAME               :   {FRAME}
    SLOT                :   {SLOT}
    PORT                :   {PORT}
    ID                  :   {ID}
    Desea continuar? [Y | N]    :   """
                ).upper()
                if keep == "Y":
                    actionList = [
                        {
                            "NOMBRE": NAME,
                            "OLT": olt,
                            "FRAME": FRAME,
                            "SLOT": SLOT,
                            "PORT": PORT,
                            "ID": ID,
                        }
                    ]
        elif lookupType == "D":
            FRAME = input("Ingrese frame de cliente : ").upper()
            SLOT = input("Ingrese slot de cliente : ").upper()
            PORT = input("Ingrese puerto de cliente : ").upper()
            ID = input("Ingrese el id del cliente : ").upper()
            command(f"display ont info {FRAME} {SLOT} {PORT} {ID} | no-more")
            sleep(3)
            value = decoder(comm)
            fail = failChecker(value)
            if fail == None:
                (_, sDESC) = check(value, "Description             : ").span()
                (eDESC, _) = check(value, "Last down cause         : ").span()
                NAME = value[sDESC:eDESC].replace("\n", "")
                keep = input(
                    f"""
    NOMBRE              :   {NAME}
    OLT                 :   {olt}
    FRAME               :   {FRAME}
    SLOT                :   {SLOT}
    PORT                :   {PORT}
    ID                  :   {ID}
    Desea continuar? [Y | N]    :   """
                ).upper()
                if keep == "Y":
                    actionList = [
                        {
                            "NOMBRE": NAME,
                            "OLT": olt,
                            "FRAME": FRAME,
                            "SLOT": SLOT,
                            "PORT": PORT,
                            "ID": ID,
                        }
                    ]
        else:
            resp = f'\nla opcion "{lookupType}" no existe\n'
            resp = colorFormatter(resp, "warning")
    else:
        resp = "\nNingun tipo de lista se ha seleccionado\n"
        resp = colorFormatter(resp, "warning")
        print(resp)
        return

    if len(actionList) > 0 and keep == "Y":
        for client in actionList:
            NOMBRE = client["NOMBRE"]
            FRAME = client["FRAME"]
            SLOT = client["SLOT"]
            PORT = client["PORT"]
            ID = client["ID"]
            OLT = client["OLT"]
            resp = (
                f"{FRAME}/{SLOT}/{PORT}/{ID} Suspendido\n"
                if "U" in typeOfList
                else f"{NOMBRE} {FRAME}/{SLOT}/{PORT}/{ID} Suspendido\n"
            )
            resp = colorFormatter(resp, "ok")
            print(resp)
            command(f"interface gpon {FRAME}/{SLOT}")
            command(f"ont deactivate {PORT} {ID}")
            command(f"display ont info {PORT} {ID}")
            if typeOfList != "RU":
                path = f"{typeOfList}_{FRAME}-{SLOT}-{PORT}-{ID}_OLT{OLT}.txt"
                sshToFile(comm, path, typeOfList)
        command("quit")
        return actionList
    else:
        resp = "\nla lista no tiene ningun cliente...\n"
        resp = colorFormatter(resp, "warning")
        print(resp)
        return
