
import os
from tkinter import filedialog
from helpers.fileFormatters.fileHandler import dictToFile
from helpers.utils.decoder import check
from helpers.utils.printer import colorFormatter, log

def verify(lst, action):
    clientLst = []
    for client in lst:
        value = open(
            f"{action}_{client['frame']}-{client['slot']}-{client['port']}-{client['id']}_OLT{client['olt']}.txt").read()
        os.remove(f"{action}_{client['frame']}-{client['slot']}-{client['port']}-{client['id']}_OLT{client['olt']}.txt")
        (_, sStatus) = check(value, "Control flag            : ").span()
        (eStatus, _) = check(value, "Run state").span()
        (_, clientSN) = check(value, "SN                      : ").span()
        STATUS = value[sStatus:eStatus-2].replace("\n", "").replace(" ", "")
        SN = value[clientSN:clientSN+16]
        obj = {
                "Cliente": client["name"],
                "Cliente/NIF":client["Cliente/NIF"],
                "Referencia":client["Referencia"],
                "Olt": client["olt"],
                "Frame": client["frame"],
                "Slot": client["slot"],
                "Puerto Olt": client["port"],
                "Onu ID": client["id"],
                "Serial del ONT": SN,
                "ID externo": client["ID"]
            }
        if SN != client["sn"]:
            val = obj
            log(colorFormatter("ALGO SALIO MAL!", "info"))
            val['odooSN'] = client['sn']
            val['Estado del contrato'] = STATUS
            clientLst.append(val)
        else:
            val = obj
            val['Estado del contrato'] = "Suspendido" if STATUS == "deactivated" else "Activo" if STATUS == "active" else None
            clientLst.append(val)
            
    log("Selecciona la lista de clientes")
    path = filedialog.askdirectory()
    dictToFile("LISTA_DE_CORTE_RESULTADOS", "E", path, clientLst, True)
    log(colorFormatter("LISTA GENERADA SATISFACTORIAMENTE","success"))