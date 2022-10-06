import re
from helpers.csvParser import converter
import os
from tkinter import filedialog

def verify(actList, action, olt):
    print("Donde quieres guardar los resultados?")
    result_path = filedialog.askdirectory()
    indexes = []
    for client in actList:
        FRAME = client["FRAME"]
        SLOT = client["SLOT"]
        PORT = client["PORT"]
        clientID = client["ID"]
        clientFile = f"{action}_{FRAME}-{SLOT}-{PORT}-{clientID}_OLT{olt}.txt"
        value = open(clientFile, "r").read()
        condition = f"""Control flag            : """
        result = re.search(condition, value)
        if(result != None):
            end = result.span()[1]
            estado = "Activo" if value[end:end + 1] == "a" else (
                "Suspendido" if value[end:end + 1] == "d" else "Ninguno")
            clientValue = {"NOMBRE": client["NOMBRE"], "Estatus": estado} if "O" not in action else {"Cliente": client["Cliente"], "Estado de contrato": estado, "ID externo": client["ID externo"], "Cliente/NIF": client["Cliente/NIF"]}
            indexes.append(clientValue)
            os.remove(f"{action}_{FRAME}-{SLOT}-{PORT}-{clientID}_OLT{olt}.txt")
        else:
            estado = "No encontrado"
            clientValue = {"NOMBRE": client["NOMBRE"], "Estatus": estado} if "O" not in action else {"Cliente": client["Cliente"], "Estado de contrato": estado, "ID externo": client["ID externo"], "Cliente/NIF": client["Cliente/NIF"]}
            indexes.append(clientValue)
            os.remove(f"{action}_{FRAME}-{SLOT}-{PORT}-{clientID}_OLT{olt}.txt")
    converter(result_path,f"resultados{olt}",indexes,True)

