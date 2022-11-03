import re
from helpers.fileHandler import toCsv
from helpers.formatter import colorFormatter
from helpers.outputDecoder import check
from helpers.failHandler import failChecker
import os
from tkinter import filedialog

condition1 = "Control flag            : "
condition2 = "Run state"


def verify(actList, action, olt):
    print("Donde quieres guardar los resultados?")
    result_path = filedialog.askdirectory()
    indexes = []
    for client in actList:
        FRAME = client["FRAME"]
        SLOT = client["SLOT"]
        PORT = client["PORT"]
        ID = client["ID"]
        value = open(f"{action}_{FRAME}-{SLOT}-{PORT}-{ID}_OLT{olt}.txt", "r").read()
        fail = failChecker(value)
        os.remove(f"{action}_{FRAME}-{SLOT}-{PORT}-{ID}_OLT{olt}.txt")
        if fail == None:
            (_, s) = check(value, condition1).span()
            (e, _) = check(value, condition2).span()
            state = value[s:e].replace("\n", "").replace(" ", "")
            estado = "suspendido" if state == "deactivated" else "activo"
            clientValue = (
                {"NOMBRE": client["NOMBRE"], "Estatus": estado}
                if "O" not in action
                else {
                    "Cliente": client["Cliente"],
                    "Estado de contrato": estado,
                    "ID externo": client["ID externo"],
                    "Cliente/NIF": client["Cliente/NIF"],
                }
            )
            indexes.append(clientValue)
        else:
            clientValue = (
                {"NOMBRE": client["NOMBRE"], "Estatus": fail}
                if "O" not in action
                else {
                    "Cliente": client["Cliente"],
                    "Estado de contrato": fail,
                    "ID externo": client["ID externo"],
                    "Cliente/NIF": client["Cliente/NIF"],
                }
            )
            indexes.append(clientValue)
    toCsv(result_path, f"resultados{olt}", indexes, True)
    resp = f'lista "resultados{olt}" creada, operacion finalizada'
    resp = colorFormatter(resp, "success")
    print(resp)
