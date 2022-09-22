import re
import csv
import os

def verifyODOO(actList, action, olt,result_path):
    indexes = []
    for client in actList:
        frame = client["frame"]
        slot = client["slot"]
        port = client["port"]
        clientID = client["id"]
        clientFile = f"{action}_{frame}-{slot}-{port}-{clientID}_OLT{olt}.txt"
        value = open(clientFile, "r").read()
        condition = f"""Control flag            : """
        result = re.search(condition, value)
        end = result.span()[1]
        estado = "Activo" if value[end:end + 1] == "a" else (
            "Suspendido" if value[end:end + 1] == "d" else "Ninguno")
        indexes.append(
            {"Cliente": client["Cliente"], "Estado de contrato": estado, "ID externo": client["ID externo"], "Cliente/NIF": client["Cliente/NIF"]})
        os.remove(f"{action}_{frame}-{slot}-{port}-{clientID}_OLT{olt}.txt")
    keys = indexes[0].keys()
    with open(f'{result_path}/resultados.csv', 'w', newline='') as f:
        dict_writer = csv.DictWriter(f, keys)
        dict_writer.writeheader()
        dict_writer.writerows(indexes)
    return indexes

def verify(actList, action, olt,result_path):
    indexes = []
    for client in actList:
        frame = client["frame"]
        slot = client["slot"]
        port = client["port"]
        clientID = client["id"]
        clientFile = f"{action}_{frame}-{slot}-{port}-{clientID}_OLT{olt}.txt"
        value = open(clientFile, "r").read()
        condition = f"""Control flag            : """
        result = re.search(condition, value)
        end = result.span()[1]
        estado = "Activo" if value[end:end + 1] == "a" else (
            "Suspendido" if value[end:end + 1] == "d" else "Ninguno")
        indexes.append(
            {"Cliente": client["Client"], "Estatus": estado})
        os.remove(f"{action}_{frame}-{slot}-{port}-{clientID}_OLT{olt}.txt")
    keys = indexes[0].keys()
    with open(f'{result_path}/resultados.csv', 'w', newline='') as f:
        dict_writer = csv.DictWriter(f, keys)
        dict_writer.writeheader()
        dict_writer.writerows(indexes)
    return indexes
