from tkinter.filedialog import askopenfilename
from helpers.fileFormatters.fileHandler import fileToDict
from helpers.info.plans import PLANS
from helpers.operations.spid import spidCalc
from helpers.utils.printer import colorFormatter, inp, log

# MODIFY THIS

def migration(comm, command, quit, olt, action):
    """
    lst should be formatted as the data object across the app
    {
      "first_name",
      "last_name",
      "nif",
      "contract",
      "olt",
      "frame",
      "slot",
      "port",
      "onu_id",
      "sn",
      "plan_name",
    }
    """
    fileType = inp("Ingrese el tipo de archivo [E | C] : ")
    fileName = askopenfilename()
    lst = fileToDict(fileName,fileType)
    for client in lst:
        plans = PLANS[client['1']]
        
        NAME = f'{client["first_name"].upper()} {client["last_name"].upper()} {client["contract"]}'
        
        command(f"interface gpon {client['frame']}/{client['slot']}")
        
        command(f'ont add {client["port"]} {client["onu_id"]} sn-auth {client["sn"]} omci ont-lineprofile-id {plans[client["plan_name"]]["line_profile"]} ont-srvprofile-id {plans[client["plan_name"]]["srv_profile"]} desc "{NAME}" ')
        
        SPID = spidCalc(client)["I"]
        
        command(
            f"ont ipconfig {client['port']} {client['onu_id']} ip-index 2 dhcp vlan {plans[client['plan']]['vlan']}"
        )
        command(
            f"ont internet-config {client['port']} {client['onu_id']} ip-index 2")
        command(
            f"ont policy-route-config {client['port']} {client['onu_id']} profile-id 2")
        command("quit")
        
        command(
            f' service-port {SPID} vlan {plans[client["plan_name"]]["vlan"]} gpon {client["frame"]}/{client["slot"]}/{client["port"]} ont {client["onu_id"]} gemport {plans[client["plan_name"]]["gem_port"]} multi-service user-vlan {plans[client["plan_name"]]["vlan"]} tag-transform transparent inbound traffic-table index {plans[client["plan_name"]]["plan"]} outbound traffic-table index {plans[client["plan_name"]]["plan"]}')
        resp = f"""
    | {NAME} {client["frame"]}/{client["slot"]}/{client["port"]}/{client["id"]}
    | {client["plan_name"]}
    Successfully Migrated!
        """
        log(colorFormatter(resp,"success"))
    quit()
    return
