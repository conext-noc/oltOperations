import pygsheets

path = "./service_account_olt_operations.json"


gc = pygsheets.authorize(service_account_file=path)
sh = gc.open("CPDC")
sh_creds = gc.open("CREDS")


wks_creds = sh_creds[0]
wks = sh[0]

cell_map = {
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

cell_map_creds = {
    "USER": "A2:A4",
    "PASS": "B2:B4",
}

def modify(lookupVal, newVal, tp):
    cell = wks.find(lookupVal)[0]
    wks.update_value(f"{cell_map[tp]}{cell.row}", newVal)

def delete(lookupVal):
    cell = wks.find(lookupVal)[0]
    wks.delete_rows(cell.row)

def insert(values):
    lst_row = len(wks.get_all_records())  + 1
    wks.insert_rows(lst_row, values=values)
    
def get_creds():
    creds = []
    users = [
        item
        for sublist in wks_creds.get_values_batch([cell_map_creds["USER"]])[0]
        for item in sublist
    ]
    passwords = [
        item
        for sublist in wks_creds.get_values_batch([cell_map_creds["PASS"]])[0]
        for item in sublist
    ]
    for idx, (user, passwd) in enumerate(zip(users, passwords)):
        creds.append(
          {f"user_{idx + 1}": user, f"password_{idx + 1}": passwd},
          )
    # users = wks_creds.get_values_batch([cell_map_creds['USER']])[0]
    return creds