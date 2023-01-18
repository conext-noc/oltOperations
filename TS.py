
from tkinter import filedialog
from helpers.fileFormatters.fileHandler import dictToFile
from helpers.utils.decoder import check
from helpers.utils.printer import colorFormatter, log


lst = [{"name": "SCRIPT MK6",
        "olt": "2",
        "frame": "0",
        "slot": "1",
        "port": "3",
        "id": "19",
        "sn": "48575443994848A5",
        }]


def verify(lst, action):
    clientLst = []
    for client in lst:
        value = open(
            f"{action}_{client['frame']}-{client['slot']}-{client['port']}-{client['id']}_OLT{client['olt']}.txt").read()
        (_, sStatus) = check(value, "Control flag            : ").span()
        (eStatus, _) = check(value, "Run state").span()
        (_, clientSN) = check(value, "SN                      : ").span()
        STATUS = value[sStatus:eStatus-2].replace("\n", "").replace(" ", "")
        SN = value[clientSN:clientSN+16]
        obj = {
                "name": client["name"],
                "olt": client["olt"],
                "frame": client["frame"],
                "slot": client["slot"],
                "port": client["port"],
                "id": client["id"],
                "sn": SN,
            }
        if SN != client["sn"]:
            val = obj
            log(colorFormatter("ALGO SALIO MAL!", "info"))
            val['odooSN'] = client['sn']
            val['status'] = STATUS
            clientLst.append(val)
        else:
            val = obj
            val['status'] = "Suspendido" if STATUS == "deactivated" else None
            clientLst.append(val)
    print(clientLst)
    log("Selecciona la lista de clientes")
    path = filedialog.askdirectory()
    dictToFile("LISTA_DE_CORTE_RESULTADOS", "E", path, clientLst, True)
    log(colorFormatter("LISTA GENERADA SATISFACTORIAMENTE","success"))

verify(lst, "SL")
