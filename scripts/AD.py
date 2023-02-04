from tkinter.filedialog import askopenfilename
from helpers.clientFinder.wan import wan
from helpers.utils.printer import colorFormatter, inp, log
from helpers.fileFormatters.fileHandler import fileToDict


def upgradeData(comm, command, quit, olt, action):
    """
    comm        :   ssh connection handler [class]
    command     :   sends ssh commands [func]
    quit        :   terminates the ssh connection [func]
    olt         :   defines the selected olt [var:str]
    action      :   defines the type of lookup/action of the client [var:str]
    
    This module starts the mass modification of clients in  olt
    
    In this module the Names and data plan of the clients will be updated
    This will require a list of clients that will contain: 
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
      "plan",
    }
    """
    fileType = inp("Ingrese el tipo de archivo [E | C] : ")
    fileName = askopenfilename()
    lst = fileToDict(fileName, fileType)
    for client in lst:
        DESC = f'{client["first_name"]} {client["last_name"]} {client["contract"]}'
        command(f"interface gpon {client['frame']}/{client['slot']}")
        command(f'ont modify {client["port"]} {client["onu_id"]} desc "{DESC}"')
        command("quit")
        (_, WAN) = wan(comm, command, client)
        for wanConf in WAN:
            command(
                f"service-port {wanConf['spid']} inbound traffic-table name {client['plan']} outbound traffic-table name {client['plan']}")
            log(colorFormatter(
                f"{DESC} {client['frame']}/{client['slot']}/{client['port']}/{client['onu_id']} tiene plan {client['plan']} en el SPID {wanConf['spid']} con la vlan {wanConf['vlan']}", "success"))
    quit()
    return
