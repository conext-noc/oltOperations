
import os
from tkinter import filedialog
from helpers.fileFormatters.fileHandler import dictToFile
from helpers.utils.decoder import check
from helpers.utils.printer import colorFormatter, log

def verify(lst, action, olt):
    clientLst = []
    for client in lst:
        OLT = str(client["olt"])[:-2] if "." in str(client["olt"]) else str(client["olt"])
        if OLT == str(olt):
            FRAME = str(client["frame"])[:-2] if "." in str(client["frame"]) else str(client["frame"])
            SLOT = str(client["slot"])[:-2] if "." in str(client["slot"]) else str(client["slot"])
            PORT = str(client["port"])[:-2] if "." in str(client["port"]) else str(client["port"])
            ID = str(client["onu_id"])[:-2] if "." in str(client["onu_id"]) else str(client["onu_id"])
            value = open(
                f"{action}_{FRAME}-{SLOT}-{PORT}-{ID}_OLT{OLT}.txt").read()
            os.remove(f"{action}_{FRAME}-{SLOT}-{PORT}-{ID}_OLT{OLT}.txt")
            (_, sStatus) = check(value, "Control flag            : ").span()
            (eStatus, _) = check(value, "Run state").span()
            (_, clientSN) = check(value, "SN                      : ").span()
            STATUS = value[sStatus:eStatus-2].replace("\n", "").replace(" ", "")
            SN = value[clientSN:clientSN+16]
            obj = {
                    "Cliente": client["name"],
                    "Referencia":client["Referencia"],
                    "Olt": client["olt"],
                    "Frame": client["frame"],
                    "Slot": client["slot"],
                    "Puerto Olt": client["port"],
                    "Onu ID": client["onu_id"],
                    "Serial del ONT": SN,
                    "Identificación externa": client["Identificación externa"],
                    "ID": client["ID"]
                }
            if SN != client["sn"]:
                val = obj
                log(colorFormatter("ALGO SALIO MAL!", "info"))
                val['odooSN'] = client['sn']
                val['Etapa'] = STATUS
                clientLst.append(val)
            else:
                val = obj
                val['Etapa'] = "Suspendido" if STATUS == "deactivated" else "Activo" if STATUS == "active" else None
                clientLst.append(val)
                
    log("Selecciona la carpeta de resultados...")
    path = filedialog.askdirectory()
    dictToFile("LISTA_DE_CORTE_RESULTADOS", "E", path, clientLst, True)
    log(colorFormatter("LISTA GENERADA SATISFACTORIAMENTE","success"))