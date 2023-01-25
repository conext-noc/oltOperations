from helpers.clientFinder.dataLookup import dataLookup
from helpers.clientFinder.nameLookup import nameLookup
from helpers.operations.addHandler import addOnuServiceNew
from helpers.utils.display import display
from helpers.utils.printer import colorFormatter, inp, log


def existingLookup(comm, command, quit, olt, action):
    """
    comm        :   ssh connection handler [class]
    command     :   sends ssh commands [func]
    quit        :   terminates the ssh connection [func]
    olt         :   defines the selected olt [var:str]
    action      :   defines the type of lookup of the client [var:str]
    """
    lookupType = inp(
        "Buscar cliente por serial, por nombre o por Datos (F/S/P/ID) [S | N | D] : "
    )
    client = (
        dataLookup(comm, command, olt, lookupType)
        if lookupType != "N"
        else nameLookup(comm, command, quit)
    )

    if client["fail"] != None:
        log(colorFormatter(client["fail"], "fail"))
        return

    if lookupType == "N":
        clients = client["data"]
        log(
            "| {:^6} | {:^3} | {:^40} | {:^10} | {:^15} | {:^16} |".format(
                "F/S/P", "ID", "NAME", "STATUS", "STATE", "SN"
            )
        )
        for client in clients:
            resp = "| {:^6} | {:^3} | {:^40} | {:^10} | {:^15} | {:^16} |".format(
                f"{client['frame']}/{client['slot']}/{client['port']}",
                client["id"],
                client["name"],
                client["runState"],
                client["controlFlag"],
                client["sn"],
            )
            log(resp)
        quit()
        return

    display(client, "B")
    # add wan profile if not exist
    # if data["wan"][0]["spid"] == None:
    #     addOnuServiceNew(comm, command, data) if olt == "1" else addOnuService(
    #         comm, command, data
    #     )
    return
