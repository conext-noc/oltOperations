from tkinter import filedialog
from helpers.clientDataLookup import lookup
from helpers.displayClient import display
from helpers.fileHandler import fromCsv
from helpers.formatter import colorFormatter
from helpers.listChecker import compare
from helpers.outputDecoder import sshToFile
from helpers.printer import inp, log

existingCond = "-----------------------------------------------------------------------------"


def deactivate(comm, command, olt, typeOfList,quit):
    actionList = []
    keep = "N"
    FAIL = None
    if "O" in typeOfList:
        log("Selecciona el archivo de lista de clientes de ODOO")
        odoo = filedialog.askopenfilename()
        log("Selecciona el archivo de lista de clientes de Drive")
        drive = filedialog.askopenfilename()
        ODOO = fromCsv(odoo)
        DRIVE = fromCsv(drive)
        actionList = compare(ODOO, DRIVE, olt)
        if(len(actionList) > 0):
            keep = "Y"
    elif "C" in typeOfList:
        log("Selecciona la lista de clientes")
        lista = filedialog.askopenfilename()
        actionList = fromCsv(lista)
        if(len(actionList) > 0):
            keep = "Y"
    elif "U" in typeOfList:
        lookupType = inp("Buscar cliente por serial o por Datos de OLT (F/S/P/ID) [S | D] : ").upper()
        data = lookup(comm, command, olt, lookupType, False)
        FAIL = data["fail"]
        if FAIL == None:
            NAME = data["name"]
            FRAME = data["frame"]
            SLOT = data["slot"]
            PORT = data["port"]
            ID = data["id"]
            OLT = olt
            proceed = display(data)
            if(proceed == "Y"):
                actionList = [{"NOMBRE":NAME,"FRAME":FRAME,"SLOT":SLOT,"PORT":PORT,"ID":ID,"OLT":OLT}]
                keep = "Y"
        else:
            resp = colorFormatter(FAIL, "fail")
            log(resp)
            quit()
            return
    else:
        resp = "\nNingun tipo de lista se ha seleccionado\n"
        resp = colorFormatter(resp, "warning")
        log(resp)
        return

    if keep == "Y":
        for client in actionList:
            NOMBRE = client["NOMBRE"]
            FRAME = client["FRAME"]
            SLOT = client["SLOT"]
            PORT = client["PORT"]
            ID = client["ID"]
            OLT = client["OLT"]
            command(f"interface gpon {FRAME}/{SLOT}")
            command(f"ont deactivate {PORT} {ID}")
            command(f"display ont info {PORT} {ID}")
            resp = (
                f"{FRAME}/{SLOT}/{PORT}/{ID} Suspendido\n"
                if "U" in typeOfList
                else f"{NOMBRE} {FRAME}/{SLOT}/{PORT}/{ID} Suspendido\n"
            )
            resp = colorFormatter(resp, "ok")
            log(resp)
            if "U" not in typeOfList:
                path = f"{typeOfList}_{FRAME}-{SLOT}-{PORT}-{ID}_OLT{OLT}.txt"
                sshToFile(comm, path, typeOfList)
                command("quit")
                return actionList
            else:
                command("quit")
                quit()
    else:
        resp = "\nla lista no tiene ningun cliente...\n"
        resp = colorFormatter(resp, "warning")
        log(resp)
        return
