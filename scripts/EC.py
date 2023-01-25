from helpers.clientFinder.dataLookup import dataLookup
from helpers.utils.display import display
from helpers.utils.printer import colorFormatter, inp, log
from helpers.utils.sheets import delete


def deleteClient(comm, command, quit, olt, action):
    """
    comm        :   ssh connection handler [class]
    command     :   sends ssh commands [func]
    quit        :   terminates the ssh connection [func]
    olt         :   defines the selected olt [var:str]
    action      :   defines the type of lookup/action of the client [var:str]
    
    This module deletes a given client
    """
    lookupType = inp("Buscar cliente por serial o por Datos (F/S/P/ID) [S | D] : ")
    client = dataLookup(comm,command,olt,lookupType)
    if client["fail"] != None:
        log(colorFormatter(client["fail"], "fail"))
        quit()
        return
    proceed = display(client,"A")
    if not proceed:
        log(colorFormatter("Cancelando...", "warning"))
        quit()
        return
    for wan in client["wan"]:
        command(f"undo service-port {wan['spid']}")
        log(f"El SPID {wan['spid']} ha sido liberado!")
    command(f"interface gpon {client['frame']}/{client['slot']}")
    command(f"ont delete {client['port']} {client['onu_id']}")
    delete(client["sn"])
    log(colorFormatter(f"El cliente {client['name']} de {client['frame']}/{client['slot']}/{client['port']}/{client['onu_id']} @ OLT {client['olt']} ha sido eliminado  ","success"))
    quit()
    return
    
