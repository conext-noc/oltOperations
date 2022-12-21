# import gspread
import pygsheets
path = "./service_account_olt_operations.json"

def wksTesting():
    gc = pygsheets.authorize(service_account_file=path)
    sh = gc.open("CPDC")
    wks = sh[3]
    cell = wks.find("4857544393CC9DA4")
    print(cell.row)

# 48575443F1839DA6 => modem router
# 485754430B0ACBA9 => bridge