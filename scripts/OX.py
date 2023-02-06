from tkinter import filedialog
from helpers.clientFinder.dataLookup import dataLookup
from helpers.clientFinder.lookup import lookup
from helpers.fileFormatters.fileHandler import fileToDict
from helpers.utils.decoder import decoder
from helpers.utils.display import display
from helpers.utils.printer import colorFormatter, inp, log
from helpers.utils.sheets import modify
from helpers.utils.verify import verify


def operate(comm, command, quit, olt, action):
    """
    comm        :   ssh connection handler [class]
    command     :   sends ssh commands [func]
    quit        :   terminates the ssh connection [func]
    olt         :   defines the selected olt [var:str]
    action      :   defines the type of lookup/action of the client [var:str]

    This module operates on a given client [reactivates | deactivates] a clients service
    """
    operation = "activate" if "R" in action else (
        "deactivate" if "S" in action else "")
    resultedAction = "Reactivado" if "R" in action else (
        "Suspendido" if "S" in action else "")
    actionList = []
    proceed = False

    if "L" in action:
        fileType = inp("Es un archivo CSV o EXCEL? [C : E]: ")
        log("Selecciona la lista de clientes...")
        fileName = filedialog.askopenfilename()
        actionList = fileToDict(fileName, fileType)
        proceed = True
    elif "U" in action:
        lookupType = inp(
            "Buscar cliente por serial o por Datos (F/S/P/ID) [S | D] : ")
        data = lookup(comm, command, olt, lookupType)
        if data["fail"] == None:
            actionList = [data]
            proceed = display(data, "A")
    else:
        log(colorFormatter("\nNingun tipo de lista se ha seleccionado\n", "warning"))
        return

    if proceed:
        for client in actionList:
            NAME = client["name"]
            FRAME = client["frame"]
            SLOT = client["slot"]
            PORT = client["port"]
            ID = client["onu_id"]
            OLT = client["olt"]
            SN = client["sn"]
            if str(OLT) == str(olt):
                command(f"interface gpon {FRAME}/{SLOT}")
                command(f"ont {operation} {PORT} {ID}")
                command(f"display ont info {PORT} {ID}")
                command("q")

                log(colorFormatter("""
    |{} 
    |{}/{}/{}/{} @ OLT {} - {}
    """.format(NAME, FRAME, SLOT, PORT, ID, OLT, resultedAction), "success"))
                output = decoder(comm)
                if "U" not in action:
                    file = f"{action}_{FRAME}-{SLOT}-{PORT}-{ID}_OLT{OLT}.txt"
                    print(output, file=open(
                        file, "a", encoding="utf-8"), flush=True)
                    print(output, file=open("suspend_log_olt.txt",
                          "a", encoding="utf-8"), flush=True)
                else:
                    modify(SN, "active", "STATUS")
        if "U" not in action:
            verify(actionList, action, olt)
        quit()
        return actionList
    else:
        log(colorFormatter("\n La Lista no tiene ningun cliente...", "warning"))
        return
