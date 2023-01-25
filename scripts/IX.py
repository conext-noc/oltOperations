from helpers.clientFinder.dataLookup import dataLookup
from helpers.clientFinder.newLookup import newLookup
from helpers.clientFinder.ontType import typeCheck
from helpers.clientFinder.optical import opticalValues
from helpers.operations.addHandler import addONUNew, addOnuServiceNew
from helpers.operations.spid import verifySPID
from helpers.utils.display import display
from helpers.utils.printer import colorFormatter, inp, log
from helpers.utils.sheets import insert
from helpers.utils.template import approved, denied
from helpers.info.plans import PLANS
from helpers.info.hashMaps import clientData


def confirmNew(comm, command, quit, olt, action):
    """
    comm        :   ssh connection handler [class]
    command     :   sends ssh commands [func]
    quit        :   terminates the ssh connection [func]
    olt         :   defines the selected olt [var:str]
    action      :   defines the type of lookup/action of installation of the client [var:str]
    
    This module adds a previous client or a new client into the olt
    """
    proceed = None
    client = clientData.copy()
    client['olt'] = olt
    if "N" in action:
        (client["sn"], FSP) = newLookup(comm, command, olt)
        val = inp("desea continuar? [Y|N] : ").upper()
        proceed = True if val == "Y" and client["sn"] != None else False
        if proceed:
            client["frame"] = int(FSP.split("/")[0])
            client["slot"] = int(FSP.split("/")[1])
            client["port"] = int(FSP.split("/")[2])

            client["plan_name"] = inp("Ingrese plan del cliente : ")

            client["line_profile"] = PLANS[client["olt"]
                                           ][client["plan_name"]]["line_profile"]
            client["srv_profile"] = PLANS[client["olt"]
                                          ][client["plan_name"]]["srv_profile"]

            client["wan"][0] = PLANS[client["olt"]][client["plan_name"]]

            client["name"] = inp("Ingrese nombre del cliente : ")[:56]
            client["nif"] = inp("Ingrese el NIF del cliente [V123 | J123]: ")

            (client["onu_id"], client["fail"]) = addONUNew(
                comm, command, client)
        else:
            log(colorFormatter("SN no aparece en OLT, Saliendo...", "warning"))
            quit()
            return

    elif "P" in action:
        lookupType = inp(
            "Buscar cliente por serial o por Datos de OLT [S | D] : ")
        client = dataLookup(comm, command, olt, lookupType)
        if client["fail"] == None:
            proceed = display(client, "I")
            client["nif"] = inp(
                "Ingrese el NIF del cliente [V123 | J123]: ").upper()

            client["plan_name"] = inp("Ingrese plan del cliente : ")

            client["line_profile"] = PLANS[client["olt"]
                                           ][client["plan_name"]]["line_profile"]
            client["srv_profile"] = PLANS[client["olt"]
                                          ][client["plan_name"]]["srv_profile"]

            client["wan"][0] = PLANS[client["olt"]][client["plan_name"]]

            command(
                f"ont modify {client['port']} {client['onu_id']} ont-lineprofile-id {client['line_profile']}")
            command(
                f"ont modify {client['port']} {client['onu_id']} ont-srvprofile-id {client['srv_profile']}")
        else:
            log(colorFormatter(client["fail"], "fail"))
            quit()
            return

    if client["onu_id"] != None and proceed:
        (client["temp"], client["pwr"]) = opticalValues(
            comm, command, client, True)

        value = inp(
            f"""
  La potencia del ONT es : {client["pwr"]} y la temperatura es : {client["temp"]}
  quieres proceder con la instalacion? [Y | N] : """
        )
        install = True if value == "Y" else False if value == "N" else None

        if not install:
            reason = inp("Por que no se le asignara servicio? : ").upper()
            denied(client, reason)
            quit()
            return
        client["device"] = typeCheck(comm, command, client)
        log(colorFormatter(
            f"El tipo de ONT del cliente es {client['device']}", "ok"))

        addOnuServiceNew(comm, command, client)

        verifySPID(comm, command, client)
        wksArr = approved(client)
        insert(wksArr)
        quit()
        return
    else:
        log(colorFormatter("Saliendo..., Cliente no se agrego en OLT", "warning"))
        quit()
        return
