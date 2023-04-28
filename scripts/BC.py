from helpers.clientFinder.lookup import lookup
from helpers.utils.display import display
from helpers.utils.printer import colorFormatter, inp, log
from helpers.utils.template import approvedDis


def existingLookup(comm, command, quit, olt, action):
    """
    comm        :   ssh connection handler [class]
    command     :   sends ssh commands [func]
    quit        :   terminates the ssh connection [func]
    olt         :   defines the selected olt [var:str]
    action      :   defines the type of lookup of the client [var:str]
    
    This module finds all the data corresponding to a given client
    """
    lookupType = inp(
        "Buscar cliente por serial, por nombre o por Datos (F/S/P/ID) [S | N | D] : "
    )
    client = lookup(comm, command, olt, lookupType)

    if client["fail"] != None:
        log(colorFormatter(client["fail"], "fail"))
        return

    if lookupType == "N":
        clients = client["data"]
        log(
            "| {:^6} | {:^7} | {:^40} | {:^10} | {:^15} | {:^16} |".format(
                "F/S/P", "ONU_ID", "NAME", "STATUS", "STATE", "SN"
            )
        )
        for client in clients:
            resp = "| {:^6} | {:^7} | {:^40} | {:^10} | {:^15} | {:^16} |".format(
                f"{client['frame']}/{client['slot']}/{client['port']}",
                client["onu_id"],
                client["name"],
                client["status"],
                client["state"],
                client["sn"],
            )
            log(resp)
        quit()
        return

    display(client, "B")
    displayTemplate = inp("Desea la plantilla de datos operacionales? [Y/N] : ").upper().strip() == 'Y'
    approvedDis(client) if displayTemplate else None
    # add wan profile if not exist
    # if client["wan"][0]["spid"] == None:
    #     addOnuServiceNew(comm, command, client)
    return
