from tkinter import filedialog
from helpers.clientDataLookup import lookup
from helpers.displayClient import display
from helpers.fileHandler import fileToDict
from helpers.printer import inp, log, colorFormatter
from helpers.outputDecoder import decoder

existingCond = "-----------------------------------------------------------------------------"


def activate(comm, command, olt, typeOfList, quit):
    actionList = []
    keep = "N"
    FAIL = None
    if "L" in typeOfList:
        fileType = inp("Es un archivo CSV o EXCEL? [C : E]: ")
        log("Selecciona la lista de clientes")
        fileName = filedialog.askopenfilename()
        actionList = fileToDict(fileName, fileType)
        keep = "Y"
    elif "U" in typeOfList:
        lookupType = inp(
            "Buscar cliente por serial o por Datos de OLT (F/S/P/ID) [S | D] : ")
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
            if (proceed == "Y"):
                actionList = [{"NOMBRE": NAME, "FRAME": FRAME,
                               "SLOT": SLOT, "PORT": PORT, "ID": ID, "OLT": OLT}]
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
            command(f"ont activate {PORT} {ID}")
            command(f"display ont info {PORT} {ID}")
            resp = (
                f"{FRAME}/{SLOT}/{PORT}/{ID} Reactivado\n"
                if "U" in typeOfList
                else f"{NOMBRE} {FRAME}/{SLOT}/{PORT}/{ID} Reactivado\n"
            )
            resp = colorFormatter(resp, "ok")
            log(resp)
            if "U" not in typeOfList:
                path = f"{typeOfList}_{FRAME}-{SLOT}-{PORT}-{ID}_OLT{OLT}.txt"
                command("quit")
                output = decoder(comm)
                print(output, file=open(path, "w"))
                return actionList
            else:
                command("quit")
                quit()
    else:
        resp = "\nla lista no tiene ningun cliente...\n"
        resp = colorFormatter(resp, "warning")
        log(resp)
        return
