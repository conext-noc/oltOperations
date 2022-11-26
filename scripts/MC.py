from helpers.formatter import colorFormatter
from helpers.clientDataLookup import lookup
from helpers.displayClient import display
from helpers.spidHandler import availableSpid
import gspread
from helpers.outputDecoder import decoder
from helpers.ontTypeHandler import typeCheck
from helpers.printer import inp, log

providerMap = {"INTER": 1101, "VNET": 1102, "PUBLICAS": 1104}

planMap = {"VLANID": "VLAN ID             : ", "PLAN": "Inbound table name  : "}

cellMap = {
    'SN': 1,
    'NAME': 2,
    'OLT': 3,
    'FRAME': 4,
    'SLOT': 5,
    'PORT': 6,
    'ID': 7,
    'ONT': 8,
    'VLAN1': 9,
    'PLAN1': 10,
    'SPID1': 11,
}


def deviceModify(comm, command, OLT,quit):
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
$ """
    ).upper()
    lookupType = inp("Buscar cliente por serial o por Datos (F/S/P/ID) [S | D] : ").upper()
    data = lookup(comm,command,OLT,lookupType)
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
        proceed = display(data)
        if (proceed == "Y"):
            if action == "CT":
                NAME = inp("Ingrese el nuevo nombre del cliente : ").upper()[:56]
                command(f" interface gpon {FRAME}/{SLOT}")
                command(f' ont modify {PORT} {ID} desc "{NAME}" ')
                command("quit")
                resp = f"Al Cliente {FRAME}/{SLOT}/{PORT}/{ID} OLT {OLT} se ha cambiado de titular a {NAME}"
                resp = colorFormatter(resp, "ok")
                log(resp)
                cell = wks.find(data["sn"])
                wks.update_cell(cell.row, cellMap["NAME"], NAME)
                quit()
                return
            if action == "CO":
                SN = inp("Ingrese el nuevo ont del cliente : ").upper()
                command(f"interface gpon {FRAME}/{SLOT}")
                command(f"ont modify {PORT} {ID} sn {SN}")
                command("quit")
                decoder(comm)
                ONT_TYPE = typeCheck(comm,command,FRAME,SLOT,PORT,ID)
                resp = f"Al Cliente 0/{SLOT}/{PORT}/{ID} OLT {OLT} se ha sido cambiado el ont a {SN}"
                resp = colorFormatter(resp, "ok")
                log(resp)
                cell = wks.find(data["sn"])
                wks.update_cell(cell.row, cellMap["SN"], SN)
                wks.update_cell(cell.row, cellMap["ONT"], ONT_TYPE)
                quit()
                return
            if action == "CV":
                PROVIDER = inp("Ingrese el nuevo proveedor de cliente [INTER | VNET] : ").upper()
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
                    command(f"ont port native-vlan {PORT} {ID} eth 1 vlan {prov}")
                    command("quit")
                resp = f"El Cliente {NAME} {FRAME}/{SLOT}/{PORT}/{ID} OLT {OLT} ha sido cambiado al proveedor {PROVIDER}"
                resp = colorFormatter(resp, "ok")
                log(resp)
                cell = wks.find(data["sn"])
                wks.update_cell(cell.row, cellMap["VLAN1"], PROVIDER)
                wks.update_cell(cell.row, cellMap["SPID1"], SPID)
                quit()
                return
            if action == "CP":
                PLAN = inp("Ingrese el nuevo plan de cliente : ").upper()
                for wanData in WAN:
                    SPID = wanData["SPID"]
                    command(f"service-port {SPID} inbound traffic-table name {PLAN} outbound traffic-table name {PLAN}")
                resp = f"El Cliente {NAME} {FRAME}/{SLOT}/{PORT}/{ID} OLT {OLT} ha sido cambiado al plan {PLAN}"
                resp = colorFormatter(resp, "ok")
                log(resp)
                cell = wks.find(data["sn"])
                wks.update_cell(cell.row, cellMap["PLAN1"], PLAN[3:])
                quit()
                return
        else:
            resp = colorFormatter("Cancelando...", "info")
            log(resp)
            quit()
            return
    else:
        resp = colorFormatter(FAIL, "warning")
        log(resp)
        quit()
        return
