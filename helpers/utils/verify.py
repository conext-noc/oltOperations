
import os
from tkinter import filedialog
from helpers.fileFormatters.fileHandler import dictToFile
from helpers.utils.decoder import check
from helpers.utils.printer import colorFormatter, log

def verify(lst, action, olt):
    clientLst = []
    for client in lst:
        if str(client["olt"]) == str(olt):
            value = open(
                f"{action}_{client['frame']}-{client['slot']}-{client['port']}-{client['onu_id']}_OLT{client['olt']}.txt").read()
            os.remove(f"{action}_{client['frame']}-{client['slot']}-{client['port']}-{client['onu_id']}_OLT{client['olt']}.txt")
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