# from time import sleep
# from tkinter.filedialog import askopenfilename
# from helpers.fileFormatters.fileHandler import fileToDict
# from helpers.utils.decoder import decoder
# from helpers.utils.printer import inp
# from helpers.utils.ssh import ssh

# def device_config():
#     ip = input("IP of device : ")
#     (comm, command, quit) = ssh(ip)
#     command("dis cu | n")
#     sleep(10)
#     output = decoder(comm)
#     device_name = input("Device name : ")
#     print(output, file=open(f"{device_name}.txt", "a"))
#     quit()
# # device_config()

# def excelTester():
#     fileType = inp("Ingrese el tipo de archivo [E | C] : ")
#     fileName = askopenfilename()
#     lst = fileToDict(fileName, fileType)
#     for client in lst:
#         print(client)
# # excelTester()

####################             IN MAINTANCE             ####################


####################             IN MAINTANCE             ####################

from tkinter import filedialog
from helpers.fileFormatters.fileHandler import dictToFile, fileToDict


def compare():
  fileOLT = "./DATA_DE_CLIENTES_OLT.xlsx"
  fileODOO = "./DATA_DE_CLIENTES_ODOO.xlsx"
  olt = fileToDict(fileOLT, "E")
  odoo = fileToDict(fileODOO, "E")
  print(olt[0])
  print(odoo[0])
  client = []
  for odooClient in odoo:
    for oltClient in olt:
      if oltClient["sn"] == odooClient["Serial del ONT"]:
        client.append({
          "name": odooClient["Cliente"],
          "contract": str(odooClient["Referencia"]).zfill(10),
          "ID externo": odooClient["ID.1"],
          "frame":oltClient["frame"],
          "slot":oltClient["slot"],
          "port":oltClient["port"],
          "onu_id":oltClient["onu_id"],
          "device":oltClient["device"],
          "sn":oltClient["sn"],
          "state":oltClient["state"],
          "olt": "La Lago"
        })
  print("Selecciona la carpeta de resultados...")
  path = filedialog.askdirectory()
  dictToFile("RESULTADO", "E", path, client, False)
compare()
