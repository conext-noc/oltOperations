####################             IN MAINTANCE             ####################

from helpers.clientFinder.dataLookup import dataLookup
from helpers.clientFinder.nameLookup import nameLookup
from helpers.utils.decoder import decoder
from helpers.utils.printer import inp
from helpers.info.hashMaps import devices
from helpers.utils.ssh import ssh


exGETReq = {
	"clients":[
		{
			"contract":"0000000245",
			"action": "R"
		},
  {
			"contract":"0000000260",
			"action": "R"
		}
	]
}

def ts():
  oltOptions = ["1", "2", "3"]
  olt = "1"
  debugging = False
  if olt in oltOptions:
      ip = "181.232.180.7"
      (comm, command, quit) = ssh(ip, debugging)
      decoder(comm)
      # new lookup by contract #
      # contract = inp("Ingrese el contrato del cliente : ")
      contract = "0000000000"
      clientData = nameLookup(comm,command, contract)
      if clientData['fail'] == None and len(clientData) != 0:
        
        # SCH
        client = dataLookup(comm, command, clientData['data'][0])
        print(client)
        
        # OPS
        client = dataLookup(comm, command, clientData['data'][0])

        # MOD
        client = dataLookup(comm, command, clientData['data'][0])
        return
      print(clientData['fail'].replace("\x1b[38;5;1m", "").replace("\x1b[0m",""))
      quit()
ts()

####################             IN MAINTANCE             ####################


####################             DATA PARSER ODOO             ####################

# from tkinter import filedialog
# from helpers.fileFormatters.fileHandler import dictToFile, fileToDict

# def compare():
#   fileOLT = "./DATA_DE_CLIENTES_OLT.xlsx"
#   fileODOO = "./DATA_DE_CLIENTES_ODOO.xlsx"
#   olt = fileToDict(fileOLT, "E")
#   odoo = fileToDict(fileODOO, "E")
#   print(olt[0])
#   print(odoo[0])
#   client = []
#   for odooClient in odoo:
#     for oltClient in olt:
#       if oltClient["sn"] == odooClient["Serial del ONT"]:
#         client.append({
#           "fsp":f'{oltClient["frame"]}/{oltClient["slot"]}/{oltClient["port"]}',
#           "frame":oltClient["frame"],
#           "slot":oltClient["slot"],
#           "port":oltClient["port"],
#           "onu_id":oltClient["onu_id"],
#           "name":odooClient["Cliente"],
#           "contract": str(odooClient["Referencia"]).zfill(10),
#           "sn":oltClient["sn"],
#           "device":oltClient["device"],
#           "ID externo": odooClient["ID.1"],
#           "state":oltClient["state"],
#           "olt": "1",
#           "plan_name":oltClient["plan_name"]
#         })
#   print("Selecciona la carpeta de resultados...")
#   path = filedialog.askdirectory()
#   dictToFile("RESULTADO", "E", path, client, False)
# compare()

####################             DATA PARSER ODOO             ####################

####################             SMART OLT REQUESTS             ####################

# import requests

# sub_domain = "conext"
# api_key="6125bdf043c44912847385f9e62ee42d"


# def activate_batch():
#   url = f"https://{sub_domain}.smartolt.com/api/onu/bulk_enable"
#   payload={
#     "onus_external_ids":"9876543210"
#   }
#   headers = {
#     'X-Token': f'{api_key}'
#   }
#   response = requests.request("POST", url, headers=headers, data=payload, files=[])
#   print(response.text)

# # activate_batch()

# def deactivate_batch():
#   url = f"https://{sub_domain}.smartolt.com/api/onu/bulk_disable"
#   payload={
#     "onus_external_ids":"9876543210"
#   }
#   headers = {
#     'X-Token': f'{api_key}'
#   }
#   response = requests.request("POST", url, headers=headers, data=payload, files=[])
#   print(response.text)

# deactivate_batch()

####################             SMART OLT REQUESTS             ####################