from datetime import datetime
from tkinter import filedialog
from helpers.clientDataLookup import lookup
from helpers.displayClient import display
from helpers.fileHandler import fileToDict
from helpers.printer import inp, log, colorFormatter
from helpers.outputDecoder import decoder
from helpers.sheets import modifier

existingCond = "-----------------------------------------------------------------------------"

def operate(comm, command, olt, action, quit):
    operation = "activate" if "R" in action else ("deactivate" if "S" in action else "")
    resultedAction = "Reactivado" if "R" in action else ("Suspendido" if "S" in action else "")
    stateAction = "active" if "R" in action else ("deactivate" if "S" in action else "")
    actionList = []
    keep = "N"
    FAIL = None
    currTime = datetime.now()
    now = f"{currTime.year}/{currTime.month}/{currTime.day} [{currTime.hour}:{currTime.minute}:{currTime.second}]"
    if "L" in action:
        fileType = inp("Es un archivo CSV o EXCEL? [C : E]: ")
        log("Selecciona la lista de clientes")
        fileName = filedialog.askopenfilename()
        actionList = fileToDict(fileName, fileType)
        print(f"LOG LISTA DE CORTE {now}\n", file=open("listLog.txt","w",encoding="utf-8"))
        keep = "Y"
    elif "U" in action:
        lookupType = inp(
            "Buscar cliente por serial o por Datos de OLT (F/S/P/ID) [S | D] : ")
        data = lookup(comm, command, olt, lookupType, False)
        FAIL = data["fail"]
        if FAIL == None:
            proceed = display(data,"A")
            if (proceed == "Y"):
                actionList = [{
                    "NOMBRE": data["name"],
                    "FRAME": data["frame"],
                    "SLOT": data["slot"],
                    "PORT": data["port"],
                    "ID": data["id"],
                    "OLT": olt,
                    "SN": data["sn"]
                }]
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
            OLT = str(client["OLT"])
            if OLT == str(olt):
                command(f"interface gpon {FRAME}/{SLOT}")
                command(f"ont {operation} {PORT} {ID}")
                command(f"display ont info {PORT} {ID}")
                command("q")
                resp = (
                    f"{FRAME}/{SLOT}/{PORT}/{ID} {resultedAction}\n"
                    if "U" in action
                    else f"{NOMBRE} {FRAME}/{SLOT}/{PORT}/{ID} OLT {OLT} {resultedAction}\n"
                )
                resp = colorFormatter(resp, "ok")
                log(resp)
                modifier("STATUS",client["SN"],stateAction)
                if "U" not in action:
                    path = f"{action}_{FRAME}-{SLOT}-{PORT}-{ID}_OLT{OLT}.txt"
                    output = decoder(comm)
                    print(output, file=open("listLog.txt","a",encoding="utf-8"))
                    print(output, file=open(path, "w",encoding="utf-8"))
        command("quit")
        quit()
        return actionList
    else:
        resp = "\nla lista no tiene ningun cliente...\n"
        resp = colorFormatter(resp, "warning")
        log(resp)
        return
