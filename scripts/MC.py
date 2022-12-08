from helpers.printer import inp, log, colorFormatter
from helpers.clientDataLookup import lookup
from helpers.displayClient import display
from helpers.spidHandler import availableSpid
import gspread
from helpers.outputDecoder import decoder
from helpers.ontTypeHandler import typeCheck
from helpers.addHandler import addOnuService
from helpers.sheets import modifier

providerMap = {"INTER": 1101, "VNET": 1102, "PUBLICAS": 1104, "VOIP": 101}

planMap = {"VLANID": "VLAN ID             : ",
           "PLAN": "Inbound table name  : "}

cellMap = {
    'SN': 1,
    'NAME': 2,
    'OLT': 3,
    'FRAME': 4,
    'SLOT': 5,
    'PORT': 6,
    'ID': 7,
    'ONT': 8,
    'STATE':9,
    'PROVIDER': 10,
    'PLAN': 11,
    'SPID': 12,
}


def deviceModify(comm, command, OLT, quit):
    sa = gspread.service_account(
        filename="service_account_olt_operations.json")
    sh = sa.open("CPDC")
    wks = sh.worksheet("DATOS")
    FRAME = ""
    SLOT = ""
    PORT = ""
    ID = ""
    NAME = ""
    FAIL = ""
    action = inp(
        """
Que cambio se realizara? 
  > (CT)    :   Cambiar Titular
  > (CO)    :   Cambiar ONT
  > (CP)    :   Cambiar Plan
  > (CV)    :   Cambiar Vlan (Proveedor)
  > (ES)    :   Eliminar Service Port
  > (AS)    :   Agregar Service Port
$ """
    ).upper()
    lookupType = inp(
        "Buscar cliente por serial o por Datos (F/S/P/ID) [S | D] : ").upper()
    data = lookup(comm, command, OLT, lookupType)
    FAIL = data["fail"]
    if FAIL == None:
        FRAME = data["frame"]
        SLOT = data["slot"]
        PORT = data["port"]
        ID = data["id"]
        NAME = data["name"]
        WAN = data["wan"]
        SPID = None
        PLAN = None
        proceed = display(data,"A")
        if (proceed == "Y"):
            command("config")
            if action == "CT":
                NAME = inp("Ingrese el nuevo nombre del cliente : ").upper()[
                    :56]
                command(f" interface gpon {FRAME}/{SLOT}")
                command(f' ont modify {PORT} {ID} desc "{NAME}" ')
                command("quit")
                resp = f"Al Cliente {FRAME}/{SLOT}/{PORT}/{ID} OLT {OLT} se ha cambiado de titular a {NAME}"
                resp = colorFormatter(resp, "ok")
                log(resp)
                modifier("NAME", data["sn"], NAME)
                quit()
                return
            if action == "CO":
                SN = inp("Ingrese el nuevo ont del cliente : ").upper()
                command(f"interface gpon {FRAME}/{SLOT}")
                command(f"ont modify {PORT} {ID} sn {SN}")
                command("quit")
                decoder(comm)
                ONT_TYPE = typeCheck(comm, command, FRAME, SLOT, PORT, ID)
                resp = f"Al Cliente 0/{SLOT}/{PORT}/{ID} OLT {OLT} se ha sido cambiado el ont a {SN}"
                resp = colorFormatter(resp, "ok")
                log(resp)
                modifier("SN", data["sn"], SN)
                modifier("ONT", data["sn"], ONT_TYPE)
                quit()
                return
            if action == "CV":
                PROVIDER = inp(
                    "Ingrese el nuevo proveedor de cliente [INTER | VNET] : ").upper()
                prov = providerMap[PROVIDER]
                for wanData in WAN:
                    SPID = wanData["SPID"]
                    PLAN = wanData["PLAN"]
                    command(f" undo  service-port  {SPID}")
                SPID = availableSpid(comm, command)
                command(
                    f"service-port {SPID} vlan {prov} gpon {FRAME}/{SLOT}/{PORT} ont {ID} gemport 14 multi-service user-vlan {prov} tag-transform transparent inbound traffic-table name {PLAN} outbound traffic-table name {PLAN}"
                )
                isBridge = inp("ONT es un bridge? [Y | N] : ").upper()
                if isBridge == "Y":
                    command(f"interface gpon {FRAME}/{SLOT}")
                    command(
                        f"ont port native-vlan {PORT} {ID} eth 1 vlan {prov}")
                    command("quit")
                resp = f"El Cliente {NAME} {FRAME}/{SLOT}/{PORT}/{ID} OLT {OLT} ha sido cambiado al proveedor {PROVIDER}"
                resp = colorFormatter(resp, "ok")
                log(resp)
                modifier("PROVIDER", data["sn"], PROVIDER)
                modifier("PLAN", data["sn"], PLAN[3:])
                modifier("SPID", data["sn"], SPID)
                quit()
                return
            if action == "CP":
                PLAN = inp("Ingrese el nuevo plan de cliente : ").upper()
                for wanData in WAN:
                    SPID = wanData["SPID"]
                    command(
                        f"service-port {SPID} inbound traffic-table name {PLAN} outbound traffic-table name {PLAN}")
                resp = f"El Cliente {NAME} {FRAME}/{SLOT}/{PORT}/{ID} OLT {OLT} ha sido cambiado al plan {PLAN}"
                resp = colorFormatter(resp, "ok")
                log(resp)
                modifier("PLAN", data["sn"], PLAN[3:])
                quit()
                return
            if action == "ES":
                log("| {:^3}| {:^4} | {:^4} | {:^10} |".format("IDX","SPID","VLAN","PLAN"))
                for idx, wanData in enumerate(data["wan"]):
                    res = colorFormatter("| {:^3}| {:^4} | {:^4} | {:^10} |".format(idx,wanData["SPID"],wanData["VLAN"],wanData["PLAN"]), "info")
                    log(res)
                spidDel = inp("Ingrese el index del SPID a eliminar : ")
                SPID_DEL = data["wan"][int(spidDel)]["SPID"]
                command(f"undo service-port {SPID_DEL}")
                
                resp = f"El Cliente {NAME} {FRAME}/{SLOT}/{PORT}/{ID} OLT {OLT} se le ha eliminado el SPID {SPID_DEL}"
                resp = colorFormatter(resp, "ok")
                modifier("PLAN", data["sn"], "")
                modifier("SPID", data["sn"], "")
                modifier("PROVIDER", data["sn"], "")
                quit()
                return
            if action == "AS":
                spidNew = availableSpid(comm, command)
                resp = f"El Cliente {NAME} {FRAME}/{SLOT}/{PORT}/{ID} OLT {OLT} se le agregara el SPID {spidNew}"
                resp = colorFormatter(resp, "info")
                PLAN = inp("Ingrese el nuevo plan de cliente : ").upper()
                PROVIDER = inp(
                    "Ingrese el nuevo proveedor de cliente [INTER | VNET | PUBLICAS | VOIP] : ").upper()
                prov = providerMap[PROVIDER]
                
                addOnuService(command,comm,spidNew,PROVIDER,FRAME,SLOT,PORT,ID,PLAN)
                resp = f"El Cliente {NAME} {FRAME}/{SLOT}/{PORT}/{ID} OLT {OLT} se le ha agregado el SPID {spidNew} con plan {PLAN} y proveedor {PROVIDER}"
                resp = colorFormatter(resp, "ok")
                modifier("PLAN", data["sn"], PLAN[3:])
                modifier("SPID", data["sn"], spidNew)
                modifier("PROVIDER", data["sn"], PROVIDER)
                quit()
                return
        else:
            resp = colorFormatter("Cancelando...", "warning")
            log(resp)
            quit()
            return
    else:
        resp = colorFormatter(FAIL, "warning")
        log(resp)
        quit()
        return
