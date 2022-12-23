import pygsheets
path = "./service_account_olt_operations.json"

cellMap = {
    'SN': "A",
    'NAME': "B",
    'CI': "C",
    'OLT': "D",
    'FRAME': "E",
    'SLOT': "F",
    'PORT': "G",
    'ID': "H",
    'ONT': "I",
    'STATUS': "J",
    'PROVIDER': "K",
    'PLAN': "L",
    'SPID': "M",
    'STATE': "N",
}
cellMapNeli = {
    '0': "C",
    '1': "AB",
    '2': "AC",
    '3': "AD",
    '4': "AE",
    '5': "AF",
    '6': "AJ",
    '7': "AT",
    '8': "AU",
}

gc = pygsheets.authorize(service_account_file=path)
# sh = gc.open("CPDC")
# wks = sh[4]
neliSh = gc.open("CO Instalaciones Oz. y MDU")
neliWks = neliSh[0]

# def modify():
#     lookupVal = input("Ingrese el valor a buscar : ")
#     newVal = input("Ingrese el nuevo valor : ")
#     tp = input("Ingrese el tipo de valor a cambiar : ")
#     cell = wks.find(lookupVal)[0]
#     wks.update_value(f"{cellMap[tp]}{cell.row}", newVal)

# def delete():
#     lookupVal = input("Ingrese el valor a buscar : ")
#     cell = wks.find(lookupVal)[0]
#     wks.delete_rows(cell.row)
    
def insertNeli(values):
    neli_lstRow = len(neliWks.get_all_records()) + 2
    for idx,value in enumerate(values):
        neliWks.update_value(f"{cellMapNeli[f'{idx}']}{neli_lstRow}", value)
    

def insert():
    values = []
    for i in range(0,9):
        val = input(f"Ingrese el valor {i} : ")
        values.append(val)
    insertNeli(values)
    # wks.insert_rows(lst_row, values=values)

insert()
    
# action = input("INGRESE ACCION : ")

# modify() if action == "M" else delete() if action == "D" else insert() if action == "I" else None