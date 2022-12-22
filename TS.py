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

gc = pygsheets.authorize(service_account_file=path)
sh = gc.open("CPDC")
wks = sh[4]

def modify():
    lookupVal = input("Ingrese el valor a buscar : ")
    newVal = input("Ingrese el nuevo valor : ")
    tp = input("Ingrese el tipo de valor a cambiar : ")
    cell = wks.find(lookupVal)[0]
    wks.update_value(f"{cellMap[tp]}{cell.row}", newVal)

def delete():
    lookupVal = input("Ingrese el valor a buscar : ")
    cell = wks.find(lookupVal)[0]
    wks.delete_rows(cell.row)

def insert():
    values = ["123","123","123","123","123","123","123","123","123","123","123","123"]
    lst_row = len(wks.get_all_records())  + 1
    wks.insert_rows(lst_row, values=values)
    
action = input("INGRESE ACCION : ")

modify() if action == "M" else delete() if action == "D" else insert() if action == "I" else None