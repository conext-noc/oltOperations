from tkinter.filedialog import askopenfilename
from helpers.fileFormatters.fileHandler import fileToDict
from helpers.info.plans import PLANS
from helpers.operations.spid import spidCalc
from helpers.utils.printer import colorFormatter, inp, log


def migration(comm, command, quit, olt, action):
    """
    comm        :   ssh connection handler [class]
    command     :   sends ssh commands [func]
    quit        :   terminates the ssh connection [func]
    olt         :   defines the selected olt [var:str]
    action      :   defines the type of lookup/action of the client [var:str]
    
    This starts the migration from olts

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
      "device"
    }
    """
    fileType = inp("Ingrese el tipo de archivo [E | C] : ")
    fileName = askopenfilename()
    lst = fileToDict(fileName, fileType)
    for client in lst:
        plans = PLANS['1']

        NAME = f'{client["first_name"].upper()} {client["last_name"].upper()} {str(client["contract"]).zfill(10)}'

        command(f"interface gpon {client['frame']}/{client['slot']}")

        command(f'ont add {client["port"]} {client["onu_id"]} sn-auth {client["sn"]} omci ont-lineprofile-id {plans[client["plan_name"]]["line_profile"]} ont-srvprofile-id {plans[client["plan_name"]]["srv_profile"]} desc "{NAME}" ')

        SPID = spidCalc(client)["I"]

        command(
            f"ont ipconfig {client['port']} {client['onu_id']} ip-index 2 dhcp vlan {plans[client['plan_name']]['vlan']}"
        )
        command(
            f"ont internet-config {client['port']} {client['onu_id']} ip-index 2")
        command(
            f"ont policy-route-config {client['port']} {client['onu_id']} profile-id 2")
        if client['device'] == "B":
            command(
                f"ont port native-vlan {client['port']} {client['onu_id']} eth 1 vlan {plans[client['plan_name']]['vlan']}")
        command("quit")

        command(
            f' service-port {SPID} vlan {plans[client["plan_name"]]["vlan"]} gpon {client["frame"]}/{client["slot"]}/{client["port"]} ont {client["onu_id"]} gemport {plans[client["plan_name"]]["gem_port"]} multi-service user-vlan {plans[client["plan_name"]]["vlan"]} tag-transform transparent inbound traffic-table index {plans[client["plan_name"]]["plan"]} outbound traffic-table index {plans[client["plan_name"]]["plan"]}')
        command(f"interface gpon {client['frame']}/{client['slot']}")
        command(
            f"ont wan-config {client['port']} {client['onu_id']} ip-index 2 profile-id 0")
        command("quit")
        resp = f"""
    | {NAME} {client["frame"]}/{client["slot"]}/{client["port"]}/{client["onu_id"]}
    | {client["plan_name"]}
    Successfully Migrated!
        """
        log(colorFormatter(resp, "success"))
    quit()
    return
