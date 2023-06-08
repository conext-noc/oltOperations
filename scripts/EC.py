from helpers.clientFinder.lookup import lookup
from helpers.utils.display import display
from helpers.utils.printer import colorFormatter, inp, log
from helpers.utils.sheets import delete
from helpers.utils.request import delete_client_data


def deleteClient(comm, command, quit_ssh, olt, _):
    """
    comm        :   ssh connection handler [class]
    command     :   sends ssh commands [func]
    quit_ssh        :   terminates the ssh connection [func]
    olt         :   defines the selected olt [var:str]
    _      :   defines the type of lookup/action of the client [var:str]

    This module deletes a given client
    """
    lookupType = inp("Buscar cliente por serial o por Datos (F/S/P/ID) [S | D] : ")
    client = lookup(comm, command, olt, lookupType)
    if client["fail"] is not None:
        log(colorFormatter(client["fail"], "fail"))
        quit_ssh()
        return
    proceed = display(client, "A")
    if not proceed:
        log(colorFormatter("Cancelando...", "warning"))
        quit_ssh()
        return
    for wan in client["wan"]:
        command(f"undo service-port {wan['spid']}")
        log(f"El SPID {wan['spid']} ha sido liberado!")
    command(f"interface gpon {client['frame']}/{client['slot']}")
    command(f"ont delete {client['port']} {client['onu_id']}")

    delete_client_data(client["sn"], "S")
    delete(client["sn"])
    log(
        colorFormatter(
            f"El cliente {client['name']} de {client['frame']}/{client['slot']}/{client['port']}/{client['onu_id']} @ OLT {client['olt']} ha sido eliminado  ",
            "success",
        )
    )
    quit_ssh()
    return
