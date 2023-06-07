import os
from dotenv import load_dotenv
from helpers.clientFinder.lookup import lookup
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
from helpers.utils.request import add_client_data

load_dotenv()


def confirmNew(comm, command, quit_ssh, olt, action):
    """
    comm        :   ssh connection handler [class]
    command     :   sends ssh commands [func]
    quit_ssh        :   terminates the ssh connection [func]
    olt         :   defines the selected olt [var:str]
    action      :   defines the type of lookup/action of installation of the client [var:str]

    This module adds a previous client or a new client into the olt
    """
    proceed = None
    client = clientData.copy()
    client["olt"] = olt
    if "N" in action:
        NEW_SN = inp("Ingrese el Serial del Cliente a buscar : ").upper()
        (client["sn"], FSP) = newLookup(comm, command, olt, NEW_SN)
        val = inp("desea continuar? [Y|N] : ").upper()
        proceed = bool(val == "Y" and client["sn"] is not None)
        if proceed:
            client["frame"] = int(FSP.split("/")[0])
            client["slot"] = int(FSP.split("/")[1])
            client["port"] = int(FSP.split("/")[2])

            client["plan_name"] = inp("Ingrese plan del cliente : ")

            ###########	OLD      ###########
            client["line_profile"] = PLANS[client["olt"]][client["plan_name"]][
                "line_profile"
            ]
            client["srv_profile"] = PLANS[client["olt"]][client["plan_name"]][
                "srv_profile"
            ]
            client["wan"][0] = PLANS[client["olt"]][client["plan_name"]]

            ###########			IP MIGRATIONS    		 ###########
            # client["line_profile"] = PLANS[client["plan_name"]]["line_profile"]
            # client["srv_profile"] = PLANS[client["plan_name"]]["srv_profile"]
            # client["wan"][0] = PLANS[client["plan_name"]]
            ###########			IP MIGRATIONS    		 ###########

            client["name"] = inp("Ingrese nombre del cliente : ")[:56]
            client["nif"] = inp("Ingrese el NIF del cliente [V123 | J123]: ")

            (client["onu_id"], client["fail"]) = addONUNew(comm, command, client)

        else:
            log(colorFormatter("SN no aparece en OLT, Saliendo...", "warning"))
            quit_ssh()

    elif "P" in action:
        lookupType = inp("Buscar cliente por serial o por Datos de OLT [S | D] : ")
        client = lookup(comm, command, olt, lookupType)
        if client["fail"] is None:
            proceed = display(client, "I")
            client["nif"] = inp("Ingrese el NIF del cliente [V123 | J123]: ").upper()

            client["plan_name"] = inp("Ingrese plan del cliente : ")

            ###########	OLD      ###########
            client["line_profile"] = PLANS[client["olt"]][client["plan_name"]][
                "line_profile"
            ]
            client["srv_profile"] = PLANS[client["olt"]][client["plan_name"]][
                "srv_profile"
            ]
            client["wan"][0] = PLANS[client["olt"]][client["plan_name"]]

            ###########			IP MIGRATIONS    		 ###########
            # client["line_profile"] = PLANS[client["plan_name"]]["line_profile"]
            # client["srv_profile"] = PLANS[client["plan_name"]]["srv_profile"]
            # client["wan"][0] = PLANS[client["plan_name"]]
            ###########			IP MIGRATIONS    		 ###########

            command(
                f"ont modify {client['port']} {client['onu_id']} ont-lineprofile-id {client['line_profile']}"
            )
            command(
                f"ont modify {client['port']} {client['onu_id']} ont-srvprofile-id {client['srv_profile']}"
            )
        log(colorFormatter(client["fail"], "fail"))
        quit_ssh()

    if client["onu_id"] is not None and proceed:
        (client["temp"], client["pwr"]) = opticalValues(comm, command, client, True)

        value = inp(
            f"""
  La potencia del ONT es : {client["pwr"]} y la temperatura es : {client["temp"]}
  quieres proceder con la instalacion? [Y | N] : """
        )
        install = True if value == "Y" else False if value == "N" else None

        if not install:
            reason = inp("Por que no se le asignara servicio? : ").upper()
            denied(client, reason)
            quit_ssh()
            return
        client["device"] = typeCheck(comm, command, client)
        log(colorFormatter(f"El tipo de ONT del cliente es {client['device']}", "ok"))

        addOnuServiceNew(comm, command, client)

        data = {
            "API_KEY": os.environ["API_KEY"],
            "client": {
                "frame": client["frame"],
                "slot": client["slot"],
                "port": client["port"],
                "onu_id": int(client["onu_id"]),
                "name": client["name"],
                "status": "online",
                "state": "active",
                "pwr": client["pwr"],
                "last_down_cause": "dying-gasp",
                "last_down_time": "-",
                "last_down_date": "-",
                "sn": client["sn"],
                "device": client["device"],
                "plan": client["plan_name"][:-2],
                "vlan": client["wan"][0]["provider"],
                "fsp": f"{client['frame']}/{client['slot']}/{client['port']}",
            },
        }
        api_response = add_client_data(data)
        if api_response.message != "User added successfully!":
            log(
                colorFormatter(
                    f"Cliente no se agrego a BD, Agg a BD Manualmente, {api_response.message} : {api_response.client.message}",
                    "warning",
                )
            )
        verifySPID(comm, command, client)
        wksArr = approved(client)
        insert(wksArr)
        quit_ssh()
        return
    log(colorFormatter("Saliendo..., Cliente no se agrego en OLT", "warning"))
    quit_ssh()
    return
