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
wks = sh[0]

def modify(lookupVal, newVal, tp):
    cell = wks.find(lookupVal)[0]
    wks.update_value(f"{cellMap[tp]}{cell.row}", newVal)

def delete(lookupVal):
    cell = wks.find(lookupVal)[0]
    wks.delete_rows(cell.row)

def insert(values):
    lst_row = len(wks.get_all_records())  + 1
    wks.insert_rows(lst_row, values=values)