import re
import csv
import os
from .listChecker import compare
from .csvParser import parser
# list1 = parser("onuOperate/LISTAS/LISTA_DE_CORTE.csv")
# list2 = parser("onuOperate/LISTAS/LISTA_DE_CLIENTES.csv")
# actionList = compare(list1, list2)


# def verifyODOO(actList, file):
#     value = open(file, "r").read()
#     indexes = []
#     for client in actList:
#         condition = """F/S/P                   : {}/{}/{}
#   ONT-ID                  : {}
#   Control flag            : """.format(client["frame"], client["slot"], client["port"], client["id"])
#         result = re.search(condition, value)
#         end = result.span()[1]
#         estado = "Activo" if value[end:end + 1] == "a" else (
#             "Suspendido" if value[end:end + 1] == "d" else "Ninguno")
#         indexes.append(
#             {"Cliente": client["Cliente"], "Estado de contrato": estado, "ID externo": client["ID externo"], "Cliente/NIF": client["Cliente/NIF"]})
#     keys = indexes[0].keys()
#     with open('resultados.csv', 'w', newline='') as f:
#         dict_writer = csv.DictWriter(f, keys)
#         dict_writer.writeheader()
#         dict_writer.writerows(indexes)
#     return indexes


def verify(actList, action, olt):
    indexes = []  # onuOperate/CLIENTES/activate_{}-{}-{}-{}_OLT{}.txt
    for client in actList:
        frame = client["frame"]
        slot = client["slot"]
        port = client["port"]
        clientID = client["id"]
        clientFile = f"{action}_{frame}-{slot}-{port}-{clientID}_OLT{olt}.txt"
        value = open(clientFile, "r").read()
        condition = f"""F/S/P                   : {frame}/{slot}/{port}
  ONT-ID                  : {clientID}
  Control flag            : """
        result = re.search(condition, value)
        end = result.span()[1]
        estado = "Activo" if value[end:end + 1] == "a" else (
            "Suspendido" if value[end:end + 1] == "d" else "Ninguno")
        indexes.append(
            {"Cliente": client["\ufeffClient"], "Estatus": estado})
        os.remove(f"{action}_{frame}-{slot}-{port}-{clientID}_OLT{olt}.txt")
    keys = indexes[0].keys()
    with open('resultados.csv', 'w', newline='') as f:
        dict_writer = csv.DictWriter(f, keys)
        dict_writer.writeheader()
        dict_writer.writerows(indexes)
    return indexes
