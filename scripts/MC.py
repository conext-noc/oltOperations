from helpers.clientFinder.lookup import lookup
from helpers.operations.addHandler import addOnuServiceNew
from helpers.operations.spid import spidCalc, verifySPID
from helpers.utils.display import display
from helpers.utils.template import change
from helpers.utils.printer import colorFormatter, inp, log
from helpers.info.plans import PLANS
from helpers.utils.sheets import modify
from helpers.clientFinder.newLookup import newLookup
from helpers.utils.request import modify_client_data


def modifyClient(comm, command, quit_ssh, olt, _):
    """
    comm        :   ssh connection handler [class]
    command     :   sends ssh commands [func]
    quit_ssh        :   terminates the ssh connection [func]
    olt         :   defines the selected olt [var:str]
    action      :   defines the type of lookup/action of the client [var:str]

    This module modifies the data of a given client
    """
    proceed = None
    action = inp(
        """
Que cambio se realizara? 
  > (CT)    :   Cambiar Titular
  > (CO)    :   Cambiar ONT
  > (CP)    :   Cambiar Plan & Vlan
  > (CV)    :   Cambiar Proveedor
  > (ES)    :   Eliminar Service Port
  > (AS)    :   Agregar Service Port
  > (AV)    :   Agregar Voip [Solo OLT 1 (X15 nueva)]
$ """
    )
    lookupType = inp("Buscar cliente por serial o por Datos (F/S/P/ID) [S | D] : ")
    # ADD NEW LOOKUP WITH DB
    client = lookup(comm, command, olt, lookupType)
    if client["fail"] is None:
        proceed = display(client, "A")
        if not proceed:
            log(colorFormatter("Cancelando...", "warning"))
            quit_ssh()
            return

        if action == "CT":
            NEW_NAME = inp("Ingrese el Nuevo Titular del cliente : ")
            command(f"interface gpon {client['frame']}/{client['slot']}")
            command(
                f'ont modify {client["port"]} {client["onu_id"]} desc "{NEW_NAME}" '
            )
            command("quit")
            msg = change(client, action, NEW_NAME)
            name_1 = NEW_NAME.split(" ")[0]
            name_2 = NEW_NAME.split(" ")[1]
            contract = NEW_NAME.split(" ")[2]
            modify_client_data(
                client["sn"],
                "S",
                "CT",
                {"name_1": name_1, "name_2": name_2, "contract": contract},
            )
            log(colorFormatter(msg, "success"))
            modify(client["sn"], NEW_NAME, "NAME")
            quit_ssh()
            return

        if action == "CO":
            SN = inp("Ingrese el Nuevo serial de ONT del cliente : ")
            (NEW_SN, _) = newLookup(comm, command, olt, SN)
            if NEW_SN is None:
                log(
                    colorFormatter(
                        f"El ONT {SN} No se encuentra en la OLT, Intente cambiar de OLT o verificar el SN",
                        "fail",
                    )
                )
                quit_ssh()
                return
            command(f"interface gpon {client['frame']}/{client['slot']}")
            command(f'ont modify {client["port"]} {client["onu_id"]} sn "{NEW_SN}" ')
            command("quit")
            msg = change(client, action, NEW_SN)
            modify_client_data(
                client["sn"],
                "S",
                "CO",
                {"sn": NEW_SN},
            )
            log(colorFormatter(msg, "success"))
            modify(client["sn"], NEW_SN, "SN")
            quit_ssh()
            return

        if action == "CP":
            for wanData in client["wan"]:
                command(f"undo service-port {wanData['spid']}")
            client["plan_name"] = inp("Ingrese el Nuevo plan a instalar : ")
            command(f"interface gpon {client['frame']}/{client['slot']}")
            ###########         OLD          ###########
            client["wan"][0] = PLANS[client["olt"]][client["plan_name"]]
            ###########         OLD          ###########

            ###########			IP MIGRATIONS    		 ###########
            # client["wan"][0] = PLANS[client["plan_name"]]
            ###########			IP MIGRATIONS    		 ###########
            command(
                f"ont modify {client['port']} {client['onu_id']} ont-lineprofile-id {client['wan'][0]['line_profile']}"
            )
            command(
                f"ont modify {client['port']} {client['onu_id']} ont-srvprofile-id {client['wan'][0]['srv_profile']}"
            )
            command("quit")
            addOnuServiceNew(comm, command, client)
            verifySPID(comm, command, client)
            msg = change(client, action, client["plan_name"])
            modify_client_data(
                client["sn"],
                "S",
                "CO",
                {"plan": client["plan_name"], "provider": client["wan"][0]["provider"]},
            )
            log(colorFormatter(msg, "success"))
            modify(client["sn"], client["plan_name"], "PLAN")
            modify(client["sn"], client["wan"][0]["vlan"], "PROVIDER")
            quit_ssh()
            return

        if action == "ES":
            log("| {:^3} | {:^4} | {:^6} |".format("IDX", "VLAN", "SPID"))
            for idx, wan in enumerate(client["wan"]):
                log("| {:^3} | {:^4} | {:^6} |".format(idx, wan["vlan"], wan["spid"]))
            DEL_SPID = int(inp("Ingrese el SPID a eliminar : "))
            command(f"undo service-port {DEL_SPID}")
            msg = change(client, action, DEL_SPID)
            log(colorFormatter(msg, "info"))
            quit_ssh()
            return

        if action == "AS":
            client["plan_name"] = inp("Ingrese el Nuevo plana instalar : ")
            client["wan"][0] = PLANS[client["olt"]][client["plan_name"]]
            addOnuServiceNew(comm, command, client)
            verifySPID(comm, command, client)
            newVal = f"{client['plan_name']} @ {client['wan'][0]['vlan']}"
            msg = change(client, action, newVal)
            log(colorFormatter(msg, "info"))
            quit_ssh()
            return

        if action == "CV":
            for wanData in client["wan"]:
                command(f"undo service-port {wanData['spid']}")
            client["plan_name"] = inp("Ingrese el Nuevo plan a instalar : ")
            ###########         OLD          ###########
            client["wan"][0] = PLANS[client["olt"]][client["plan_name"]]
            ###########         OLD          ###########

            ###########			IP MIGRATIONS    		 ###########
            # client["wan"][0] = PLANS[client["plan_name"]]
            ###########			IP MIGRATIONS    		 ###########
            addOnuServiceNew(comm, command, client)
            verifySPID(comm, command, client)
            msg = change(client, action, client["plan_name"])
            modify_client_data(
                client["sn"],
                "S",
                "CO",
                {"plan": client["plan_name"], "provider": client["wan"][0]["provider"]},
            )
            log(colorFormatter(msg, "info"))
            quit_ssh()
            return

        if action == "AV":
            client["wan"][0]["spid"] = spidCalc(client)["V"]
            log(
                colorFormatter(
                    f"SPID PARA AGG {client['spid']}, FUNCION AUN NO DISPONIBLE", "info"
                )
            )
            quit_ssh()
            return
    else:
        log(colorFormatter(f"{client['fail']}", "fail"))
