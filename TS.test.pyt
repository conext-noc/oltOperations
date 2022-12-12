from helpers.printer import colorFormatter
import gspread
from helpers.displayClient import display

def delete(OLT = 9):
    sa = gspread.service_account(
        filename="service_account_olt_operations.json")
    sh = sa.open("CPDC")
    wks = sh.worksheet("DATOS")
    data = {
      "fail":None,
      "frame":0,
      "slot":0,
      "port":0,
      "id":0,
      "name":"testing",
      "status":"active",
      "state":"online",
      "ldc":"los",
      "temp":30,
      "pwr":-24.35,
      "ipAdd":"10.10.10.10",
      "wan":[
        {"SPID":123,"PLAN":"TEST","VLAN":"8000"}
      ],
      "sn":"0123456789ABCDEF",
    }
    if data["fail"] == None:
        proceed = display(data,"A")
        if proceed == "Y":
            FRAME = data["frame"]
            SLOT = data["slot"]
            PORT = data["port"]
            ID = data["id"]
            NAME = data["name"]
            SN = data["sn"]
            for wanData in data["wan"]:
                spid = wanData["SPID"]
                print(f" undo  service-port  {spid}")
            print(f"interface gpon {FRAME}/{SLOT}")
            print(f"ont delete {PORT} {ID}")
            print("quit")
            resp = colorFormatter(
                f"{NAME} {FRAME}/{SLOT}/{PORT}/{ID} de OLT {OLT} ha sido eliminado", "ok")
            cell = wks.find(SN)
            wks.delete_row(cell.row)
            print(resp)
            return
    else:
        fail = colorFormatter(data["fail"], "fail")
        print(fail)
