from tkinter import filedialog
from helpers.clientFinder.lookup import lookup
from helpers.fileFormatters.fileHandler import fileToDict
from helpers.utils.decoder import decoder
from helpers.utils.display import display
from helpers.utils.printer import colorFormatter, inp, log
from helpers.utils.sheets import modify
from helpers.utils.verify import verify
from helpers.utils.request import modify_client_data


def operate(comm, command, quit_ssh, olt, action):
    """
    comm        :   ssh connection handler [class]
    command     :   sends ssh commands [func]
    quit_ssh        :   terminates the ssh connection [func]
    olt         :   defines the selected olt [var:str]
    action      :   defines the type of lookup/action of the client [var:str]

    This module operates on a given client [reactivates | deactivates] a clients service
    """
    operation = "activate" if "R" in action else ("deactivate" if "S" in action else "")
    resultedAction = (
        "Reactivado" if "R" in action else ("Suspendido" if "S" in action else "")
    )
    resultedActionDB = (
        "active" if "R" in action else ("deactivated" if "S" in action else "")
    )
    actionList = []
    proceed = False

    if "L" in action:
        fileType = inp("Es un archivo CSV o EXCEL? [C : E]: ")
        log("Selecciona la lista de clientes...")
        fileName = filedialog.askopenfilename()
        actionList = fileToDict(fileName, fileType)
        proceed = True
    elif "U" in action:
        lookupType = inp("Buscar cliente por serial o por Datos (F/S/P/ID) [S | D] : ")
        data = lookup(comm, command, olt, lookupType)
        # AGG NEW LOOKUP FUNC
        if data["fail"] is None:
            actionList = [data]
            proceed = display(data, "A")
    else:
        log(colorFormatter("\nNingun tipo de lista se ha seleccionado\n", "warning"))
        return

    if proceed:
        for client in actionList:
            NAME = str(client["name"])
            FRAME = (
                str(client["frame"])[:-2]
                if "." in str(client["frame"])
                else str(client["frame"])
            )
            SLOT = (
                str(client["slot"])[:-2]
                if "." in str(client["slot"])
                else str(client["slot"])
            )
            PORT = (
                str(client["port"])[:-2]
                if "." in str(client["port"])
                else str(client["port"])
            )
            ID = (
                str(client["onu_id"])[:-2]
                if "." in str(client["onu_id"])
                else str(client["onu_id"])
            )
            OLT = (
                str(client["olt"])[:-2]
                if "." in str(client["olt"])
                else str(client["olt"])
            )
            SN = str(client["sn"])
            if str(OLT) == str(olt):
                command(f"interface gpon {FRAME}/{SLOT}")
                command(f"ont {operation} {PORT} {ID}")
                command(f"display ont info {PORT} {ID}")
                command("q")
                command("quit")

                log(
                    colorFormatter(
                        f"""
    |{NAME} 
    |{FRAME}/{SLOT}/{PORT}/{ID} @ OLT {OLT} - {resultedAction}
    """,
                        "success",
                    )
                )
                output = decoder(comm)

                api_response = modify_client_data(
                    SN, "S", "OX", {"state": resultedActionDB}
                )
                log(
                    colorFormatter(
                        f"Cliente no se modifico en BD, Modificar en BD Manualmente, {api_response.message} : {api_response.client.message}",
                        "warning",
                    )
                ) if api_response.message != "Client updated successfully!" else log(
                    colorFormatter(
                        "Cliente modificado en BD.",
                        "success",
                    )
                )
                if "U" not in action:
                    file = f"{action}_{FRAME}-{SLOT}-{PORT}-{ID}_OLT{OLT}.txt"
                    print(output, file=open(file, "a", encoding="utf-8"), flush=True)
                    print(
                        output,
                        file=open("suspend_log_olt.txt", "a", encoding="utf-8"),
                        flush=True,
                    )
                else:
                    modify(SN, "active", "STATUS")
        if "U" not in action:
            verify(actionList, action, olt)
        quit_ssh()
        return actionList
    log(colorFormatter("\n La Lista no tiene ningun cliente...", "warning"))
    return
