from helpers.getWanData import wan
from helpers.serialLookup import serialSearch
from helpers.outputDecoder import decoder, check
from helpers.formatter import colorFormatter
from helpers.failHandler import failChecker
from helpers.getONTSpid import getOntSpid
from time import sleep

providerMap = {"INTER": 1101, "VNET": 1102, "PUBLICAS": 1104}

planMap = {"VLANID": "VLAN ID             : ", "PLAN": "Inbound table name  : "}


def deviceModify(comm, command, OLT):
    FRAME = ""
    SLOT = ""
    PORT = ""
    ID = ""
    NAME = ""
    FAIL = None
    action = input(
        """
Que cambio se realizara? 
  > (CT)    :   Cambiar Titular
  > (CO)    :   Cambiar ONT
  > (CP)    :   Cambiar Plan
  > (CV)    :   Cambiar Vlan (Proveedor)
$ """
    ).upper()
    lookupType = input(
        "Buscar cliente por serial o por Datos (F/S/P/ID) [S | D] : "
    ).upper()
    if lookupType == "S":
        SN = input("Ingrese el Serial del Cliente a buscar : ").upper()
        (FRAME, SLOT, PORT, ID, NAME, STATE, FAIL) = serialSearch(comm, command, SN)
        if FAIL == None:
            keep = input(
                f"""
        NOMBRE              :   {NAME}
        OLT                 :   {OLT}
        FRAME               :   {FRAME}
        SLOT                :   {SLOT}
        PORT                :   {PORT}
        ID                  :   {ID}
        Desea continuar? [Y | N]    :   """
            ).upper()
            FAIL = (
                None
                if keep == "Y"
                else (
                    "No se procedera con la operacion..."
                    if keep == "N"
                    else f"opcion {keep} no existe"
                )
            )
    if lookupType == "D":
        FRAME = input("Ingrese frame de cliente : ").upper()
        SLOT = input("Ingrese slot de cliente : ").upper()
        PORT = input("Ingrese puerto de cliente : ").upper()
        ID = input("Ingrese el id del cliente : ").upper()
        command(f"display ont info {FRAME} {SLOT} {PORT} {ID} | no-more")
        sleep(3)
        value = decoder(comm)
        fail = failChecker(value)
        if fail == None:
            (_, sDESC) = check(value, "Description             : ").span()
            (eDESC, _) = check(value, "Last down cause         : ").span()
            NAME = value[sDESC:eDESC].replace("\n", "")
            keep = input(
                f"""
    NOMBRE              :   {NAME}
    OLT                 :   {OLT}
    FRAME               :   {FRAME}
    SLOT                :   {SLOT}
    PORT                :   {PORT}
    ID                  :   {ID}
    Desea continuar? [Y | N]    :   """
            ).upper()
            FAIL = (
                None
                if keep == "Y"
                else (
                    "No se procedera con la operacion..."
                    if keep == "N"
                    else f"opcion {keep} no existe"
                )
            )
    if FAIL == None:
        if action == "CT":
            command(f"interface gpon {FRAME}/{SLOT}")
            NAME = input("Ingrese el nuevo nombre del cliente : ").upper()
            command(f"ont modify {PORT} {ID} desc {NAME}")
            command("quit")
            resp = f"Al Cliente {FRAME}/{SLOT}/{PORT}/{ID} OLT {OLT} se ha cambiado de titular a {NAME}"
            resp = colorFormatter(resp, "ok")
            print(resp)
            return
        if action == "CO":
            command(f"interface gpon {FRAME}/{SLOT}")
            SN = input("Ingrese el nuevo ont del cliente : ").upper()
            command(f"ont modify {PORT} {ID} sn {SN}")
            command("quit")
            resp = f"Al Cliente 0/{SLOT}/{PORT}/{ID} OLT {OLT} se ha sido cambiado el ont a {SN}"
            resp = colorFormatter(resp, "ok")
            print(resp)
            return
        if action == "CV":
            (VLAN, PLAN, IPADDRESS, SPID) = wan(comm, command, FRAME, SLOT, PORT, ID)
            print(
                f"""
            NOMBRE DE CLIENTE   :   {NAME}
            VLAN DE CLIENTE     :   {VLAN}
            PLAN DE CLIENTE     :   {PLAN}
            IP DEL CLIENTE      :   {IPADDRESS}
            SPID                :   {SPID}
            """
            )
            PROVIDER = input(
                "Ingrese el nuevo proveedor de cliente [INTER | VNET] : "
            ).upper()
            prov = providerMap[PROVIDER]
            command(f" undo  service-port  {SPID}")
            command(
                f"service-port {SPID} vlan {prov} gpon {FRAME}/{SLOT}/{PORT} ont {ID} gemport 14 multi-service user-vlan {prov} tag-transform transparent inbound traffic-table name {PLAN} outbound traffic-table name {PLAN}"
            )
            isBridge = input("ONT es un bridge? [Y | N] : ").upper()
            if isBridge == "Y":
                command(f"interface gpon {FRAME}/{SLOT}")
                command(f"ont port native-vlan {PORT} {ID} eth 1 vlan {prov}")
                command("quit")
            resp = f"El Cliente {NAME} {FRAME}/{SLOT}/{PORT}/{ID} OLT {OLT} ha sido cambiado al proveedor {PROVIDER}"
            resp = colorFormatter(resp, "ok")
            print(resp)
            return
        if action == "CP":
            (VLAN, PLAN, IPADDRESS, SPID) = wan(comm, command, FRAME, SLOT, PORT, ID)
            print(
                f"""
            NOMBRE DE CLIENTE   :   {NAME}
            VLAN DE CLIENTE     :   {VLAN}
            PLAN DE CLIENTE     :   {PLAN}
            IP DEL CLIENTE      :   {IPADDRESS}
            SPID                :   {SPID}
            """
            )
            PLAN = input("Ingrese el nuevo plan de cliente : ").upper()
            result = getOntSpid(comm, command, FRAME, SLOT, PORT, ID)
            if result["ttl"] == 2:
                spid1 = result["values"][0]
                spid2 = result["values"][1]
                command(
                    f"service-port {spid1} inbound traffic-table name {PLAN} outbound traffic-table name {PLAN}"
                )
                command(
                    f"service-port {spid2} inbound traffic-table name {PLAN} outbound traffic-table name {PLAN}"
                )
            if result["ttl"] == 1:
                spid = result["values"]
                command(
                    f"service-port {spid} inbound traffic-table name {PLAN} outbound traffic-table name {PLAN}"
                )
            resp = f"El Cliente {NAME} {FRAME}/{SLOT}/{PORT}/{ID} OLT {OLT} ha sido cambiado al plan {PLAN}"
            resp = colorFormatter(resp, "ok")
            print(resp)
            return
    else:
        resp = colorFormatter(FAIL, "warning")
        print(resp)
        return
