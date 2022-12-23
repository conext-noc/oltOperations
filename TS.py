import pygsheets
path = "./service_account_olt_operations.json"

gc = pygsheets.authorize(service_account_file=path)
sh = gc.open("CPDC")
wks = sh[0]
neliSh = gc.open("CO Instalaciones Oz. y MDU")
neliWks = neliSh[0]


print(wks,neliWks)