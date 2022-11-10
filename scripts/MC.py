from helpers.getWanData import wan
from helpers.serialLookup import serialSearch
from helpers.outputDecoder import decoder, check
from helpers.formatter import colorFormatter
from helpers.failHandler import failChecker
from helpers.spidHandler import ontSpid
from re import sub
from time import sleep
from helpers.clientDataLookup import lookup

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
    lookupType = input("Buscar cliente por serial o por Datos (F/S/P/ID) [S | D] : ").upper()
    data = lookup(comm,command,OLT,lookupType)
    if data["fail"] == None:
        FRAME = data["frame"]
        SLOT = data["slot"]
        PORT = data["port"]
        ID = data["id"]
        NAME = data["name"]
        IPADDRESS = data["ipAdd"]
        WAN = data["wan"]
        STATE = data["state"]
        TEMP = data["temp"]
        PWR = data["pwr"]
        str1 = f"""
    FRAME               :   {FRAME}
    SLOT                :   {SLOT}
    PORT                :   {PORT}
    ID                  :   {ID}
    NAME                :   {NAME}
    SN                  :   {data["sn"]}
    STATE               :   {STATE}
    STATUS              :   {data["status"]}
    LAST DOWN CAUSE     :   {data["ldc"]}
    ONT TYPE            :   {data["type"]}
    IP                  :   {IPADDRESS}
    TEMPERATURA         :   {TEMP}
    POTENCIA            :   {PWR}
                """
        str2 = ""
        for idx, wanData in enumerate(WAN):
                str2 += f"""
    VLAN_{idx}              :   {wanData["VLAN"]}
    PLAN_{idx}              :   {wanData["PLAN"]}
    SPID_{idx}              :   {wanData["SPID"]}
                """
        res = str1 + str2
        res = colorFormatter(res, "ok")
        print(res)
        if action == "CT":
            command(f"  interface  gpon  {FRAME}/{SLOT}")
            NAME = input("Ingrese el nuevo nombre del cliente : ").upper()
            command(f"  ont  modify  {PORT}  {ID}  desc  '{NAME}'  ")
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
            SPID = WAN[0]["SPID"]
            PLAN = WAN[0]["PLAN"]
            PROVIDER = input("Ingrese el nuevo proveedor de cliente [INTER | VNET] : ").upper()
            prov = providerMap[PROVIDER]
            for wanData in WAN:
                spid = wanData["SPID"]
                command(f" undo  service-port  {spid}")

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
            PLAN = input("Ingrese el nuevo plan de cliente : ").upper()
            for wanData in WAN:
                spid = wanData["SPID"]
                command(f" undo  service-port  {spid}")
            spid = WAN[0]["SPID"]
            command(f"service-port {spid} inbound traffic-table name {PLAN} outbound traffic-table name {PLAN}")
            resp = f"El Cliente {NAME} {FRAME}/{SLOT}/{PORT}/{ID} OLT {OLT} ha sido cambiado al plan {PLAN}"
            resp = colorFormatter(resp, "ok")
            print(resp)
            return
    else:
        resp = colorFormatter(FAIL, "warning")
        print(resp)
        return
