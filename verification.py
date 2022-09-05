import re
import csv
from listChecker import compare
from csvParser import parser
list1 = parser("LISTAS/LISTA_DE_CORTE.csv")
list2 = parser("LISTAS/LISTA_DE_CLIENTES.csv")
actionList = compare(list1, list2)


def verify(actList, file):
    value = open(file, "r").read()
    indexes = []
    for client in actList:
        condition = """F/S/P                   : {}/{}/{}
  ONT-ID                  : {}
  Control flag            : """.format(client["frame"], client["slot"], client["port"], client["id"])
        result = re.search(condition, value)
        end = result.span()[1]
        estado = "Activo" if value[end:end + 1] == "a" else (
            "Suspendido" if value[end:end + 1] == "d" else "Ninguno")
        indexes.append(
            {"Cliente": client["nombre"], "Estado de contrato": estado})
    keys = indexes[0].keys()
    with open('resultados.csv', 'w', newline='') as f:
        dict_writer = csv.DictWriter(f, keys)
        dict_writer.writeheader()
        dict_writer.writerows(indexes)
    return indexes
