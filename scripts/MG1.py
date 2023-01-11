from tkinter.filedialog import askopenfilename
from helpers.fileFormatters.fileHandler import fileToDict
from helpers.info.plans import PLANS, plans
from helpers.operations.spid import spidCalc
from helpers.utils.printer import colorFormatter, inp, log

# MODIFY THIS

def migration(comm, command, quit, olt, action):
    """"
    lst should be formatted as the data object across the app
    {
      "fName",
      "lName",
      "nif",
      "contract",
      "olt",
      "frame",
      "slot",
      "port",
      "id",
      "sn",
      "plan",
    }
    """
    fileType = inp("Ingrese el tipo de archivo [E | C] : ")
    fileName = askopenfilename()
    lst = fileToDict(fileName,fileType)
    for client in lst:
        NAME = f'{client["fName"].upper()} {client["lName"].upper()} {client["contract"]}'
        command(f"interface gpon {client['frame']}/{client['slot']}")
        command(f'ont add {client["port"]} {client["id"]} sn-auth {client["sn"]} omci ont-lineprofile-id {plans[client["plan"]]["lineProfile"]} ont-srvprofile-id {plans[client["plan"]]["srvProfile"]} desc "{NAME}" ')
        SPID = spidCalc(client)["I"]
        command(
            f"ont ipconfig {client['port']} {client['id']} ip-index 2 dhcp vlan {plans[client['plan']]['vlan']}"
        )
        command(
            f"ont internet-config {client['port']} {client['id']} ip-index 2")
        command(
            f"ont policy-route-config {client['port']} {client['id']} profile-id 2")
        command("quit")
        command(
            f' service-port {SPID} vlan {PLANS[client["olt"]][client["plan"]]["vlan"]} gpon {client["frame"]}/{client["slot"]}/{client["port"]} ont {client["id"]} gemport {PLANS[client["olt"]][client["plan"]]["gemPort"]} multi-service user-vlan {PLANS[client["olt"]][client["plan"]]["vlan"]} tag-transform transparent inbound traffic-table index {PLANS[client["olt"]][client["plan"]]["vlan"]} outbound traffic-table index {PLANS[client["olt"]][client["plan"]]["vlan"]}')
        resp = f"""
    | {NAME} {client["frame"]}/{client["slot"]}/{client["port"]}/{client["id"]}
    | {client["plan"]}
    Successfully Migrated!
        """
        log(colorFormatter(resp,"success"))
    quit()
    return