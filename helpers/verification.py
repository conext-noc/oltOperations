import re
import csv
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
        end = result.span()[1]
        estado = "Activo" if value[end:end + 1] == "a" else (
            "Suspendido" if value[end:end + 1] == "d" else "Ninguno")
        clientValue = {"NOMBRE": client["NOMBRE"], "Estatus": estado} if "O" not in action else {"Cliente": client["Cliente"], "Estado de contrato": estado, "ID externo": client["ID externo"], "Cliente/NIF": client["Cliente/NIF"]}
        indexes.append(clientValue)
        os.remove(f"{action}_{FRAME}-{SLOT}-{PORT}-{clientID}_OLT{olt}.txt")
    keys = indexes[0].keys()
    with open(f'{result_path}/resultados.csv', 'w', newline='') as f:
        dict_writer = csv.DictWriter(f, keys)
        dict_writer.writeheader()
        dict_writer.writerows(indexes)
    return indexes
