from helpers.printer import colorFormatter, inp, log
from helpers.spidHandler import availableSpid, ontSpid
from helpers.addHandler import addOnuService
from tkinter import filedialog
from helpers.fileHandler import fileToDict


providerMap = {"INTER": 1101, "VNET": 1102, "PUBLICAS": 1104}

planMap = {"VLANID": "VLAN ID             : ",
           "PLAN": "Inbound table name  : "}

def planChanger(comm, command, quit, olt):
    CLIENTS = []
    fileType = inp("Es un archivo CSV o EXCEL? [C : E]: ")
    log("Selecciona la lista con datos de Odoo")
    fileName = filedialog.askopenfilename()
    lst = fileToDict(fileName, fileType)
    
    for (idx, client) in enumerate(lst):
        OLT = client["OLT"]
        if olt == OLT:
            FAIL = None
            FRAME = client["FRAME"]
            SLOT = client["SLOT"]
            PORT = client["PORT"]
            ID = client["ID"]
            NAME = client["NAME"]
            PROVIDER = client["PROVIDER"]
            VLAN = providerMap[PROVIDER]
            PLAN = client["PLAN"]
            (data, FAIL) = ontSpid(comm, command, FRAME, SLOT, PORT, ID)
            if FAIL == None:
                for spidData in data:
                    SPID = spidData["SPID"]
                    command(f"undo service-port {SPID}")
                newSpid = availableSpid()
                addOnuService(command, comm, newSpid, VLAN,
                              FRAME, SLOT, PORT, ID, PLAN)
                log(colorFormatter(
                    f"{idx} Cliente {NAME} @ {FRAME}/{SLOT}/{PORT}/{ID} OLT {OLT} se le ha cambiado el proveedor y plan a {PROVIDER}({VLAN})-{PLAN}", "info"))
                CLIENTS.append({
                  "NAME":NAME,
                  "OLT":OLT,
                  "FRAME":FRAME,
                  "SLOT":SLOT,
                  "PORT":PORT,
                  "ID":ID,
                  "VLAN":VLAN,
                  "PROVIDER":PROVIDER,
                  "PLAN":PLAN,
                  })
            else:
                log(FAIL)
    quit()
    return CLIENTS