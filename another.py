from listChecker import compare
from csvParser import parser
import csv
list1 = parser("LISTA_DE_CORTE.csv")
list2 = parser("LISTA_DE_CLIENTES.csv")

dataList = []

for client in list2:
    if (client["olt"] == "2"):
        dataList.append(client)

# print(dataList)
# print(list1)

data = compare(list1, dataList)

# for c in data:
#     print(c)

keys = data[0].keys()

# print(data)

with open('LISTA_DE_CORTE_OLT2.csv', 'w', newline='') as f:
    dict_writer = csv.DictWriter(f, keys)
    dict_writer.writeheader()
    dict_writer.writerows(data)
