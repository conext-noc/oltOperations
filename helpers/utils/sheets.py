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
sh = gc.open("CPDC")
wks = sh[0]
neliSh = gc.open("CO Instalaciones Oz. y MDU")
neliWks = neliSh[0]

    
def insertNeli(values):
    vals = [values[2],values[3],values[4],values[5],values[6],values[7],values[0],values[14],f"{values[15]}°C"]
    neli_lstRow = len(neliWks.get_all_records()) + 2
    for idx,value in enumerate(vals):
        neliWks.update_value(f"{cellMapNeli[f'{idx}']}{neli_lstRow}", value)
    

def modify(lookupVal, newVal, tp):
    cell = wks.find(lookupVal)[0]
    wks.update_value(f"{cellMap[tp]}{cell.row}", newVal)

def delete(lookupVal):
    cell = wks.find(lookupVal)[0]
    wks.delete_rows(cell.row)

def insert(values):
    vals = []
    for idx,value in enumerate(values):
        if idx <= 12:
            vals.append(value)
    lst_row = len(wks.get_all_records())  + 1
    wks.insert_rows(lst_row, values=vals)
    insertNeli(values)