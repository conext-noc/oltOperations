from time import sleep
from helpers.outputDecoder import decoder
from helpers.serviceMaper import plans, spidCalc
from helpers.displayClient import display
from helpers.ontTypeHandler import typeCheck
from helpers.spidHandler import verifySPID
from helpers.opticalCheck import opticalValues
from helpers.printer import inp, log, colorFormatter
from helpers.clientDataLookup import lookup, newLookup
from helpers.addHandler import addONU, addOnuServiceNew
from helpers.printer import colorFormatter
import gspread
import pygsheets
path = "./service_account_olt_operations.json"

# def testing(OLT = 9):
#     gc = pygsheets.authorize(service_account_file=path)
#     shTest = gc.open("CPDC")
#     wkshTest = shTest[0]
#     print(wkshTest.cell("A2"))
#     sa = gspread.service_account(
#         filename="service_account_olt_operations.json")
#     sh = sa.open("CPDC")
#     wks = sh.worksheet("DATOS")
#     data = {
#       "fail":None,
#       "frame":0,
#       "slot":0,
#       "port":0,
#       "id":0,
#       "type":"EchoLife EG8141A5",
#       "name":"testing",
#       "status":"active",
#       "state":"online",
#       "ldc":"los",
#       "temp":30,
#       "pwr":-24.35,
#       "ipAdd":"10.10.10.10",
#       "wan":[
#         {"SPID":123,"PLAN":"TEST","VLAN":"8000"}
#       ],
#       "sn":"0123456789ABCDEF",
#     }
#     if data["fail"] == None:
#         print(data)
#         proceed = "Y"
#         if proceed == "Y":
#             FRAME = data["frame"]
#             SLOT = data["slot"]
#             PORT = data["port"]
#             ID = data["id"]
#             NAME = data["name"]
#             SN = data["sn"]
#             for wanData in data["wan"]:
#                 spid = wanData["SPID"]
#                 print(f" undo  service-port  {spid}")
#             print(f"interface gpon {FRAME}/{SLOT}")
#             print(f"ont delete {PORT} {ID}")
#             print("quit")
#             resp = colorFormatter(
#                 f"{NAME} {FRAME}/{SLOT}/{PORT}/{ID} de OLT {OLT} ha sido eliminado", "ok")
#             cell = wks.find(SN)
#             print(cell.row)
#             wks.delete_rows(cell.row)
#             print(resp)
#             return
#     else:
#         fail = colorFormatter(data["fail"], "fail")
#         print(fail)
# def wksTesting():
#     gc = pygsheets.authorize(service_account_file=path)
#     sh = gc.open("CPDC")
#     wks = sh[3]
#     cell = wks.find("4857544393CC9DA4")
#     print(cell.row)

# 48575443F1839DA6 => modem router
# 485754430B0ACBA9 => bridge