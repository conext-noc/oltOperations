from helpers.formatter import colorFormatter
from helpers.clientDataLookup import lookup
from helpers.displayClient import display
from helpers.spidHandler import availableSpid

providerMap = {"INTER": 1101, "VNET": 1102, "PUBLICAS": 1104}

planMap = {"VLANID": "VLAN ID             : ", "PLAN": "Inbound table name  : "}


def deviceModify(comm, command, OLT,quit):
    FRAME = ""
    SLOT = ""
    PORT = ""
    ID = ""
    NAME = ""
    FAIL = ""
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
                NAME = input("Ingrese el nuevo nombre del cliente : ").upper()
                command(f" interface gpon {FRAME}/{SLOT}")
                command(f' ont modify {PORT} {ID} desc "{NAME}" ')
                command("quit")
                resp = f"Al Cliente {FRAME}/{SLOT}/{PORT}/{ID} OLT {OLT} se ha cambiado de titular a {NAME}"
                resp = colorFormatter(resp, "ok")
                print(resp)
                quit(5)
                return
            if action == "CO":
                SN = input("Ingrese el nuevo ont del cliente : ").upper()
                command(f"interface gpon {FRAME}/{SLOT}")
                command(f"ont modify {PORT} {ID} sn {SN}")
                command("quit")
                resp = f"Al Cliente 0/{SLOT}/{PORT}/{ID} OLT {OLT} se ha sido cambiado el ont a {SN}"
                resp = colorFormatter(resp, "ok")
                print(resp)
                quit(5)
                return
            if action == "CV":
                PROVIDER = input("Ingrese el nuevo proveedor de cliente [INTER | VNET] : ").upper()
                prov = providerMap[PROVIDER]
                for wanData in WAN:
                    SPID = wanData["SPID"]
                    PLAN = wanData["PLAN"]
                    command(f" undo  service-port  {SPID}")
                SPID = availableSpid(comm, command)
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
                quit(5)
                return
            if action == "CP":
                PLAN = input("Ingrese el nuevo plan de cliente : ").upper()
                for wanData in WAN:
                    SPID = wanData["SPID"]
                    command(f"service-port {SPID} inbound traffic-table name {PLAN} outbound traffic-table name {PLAN}")
                resp = f"El Cliente {NAME} {FRAME}/{SLOT}/{PORT}/{ID} OLT {OLT} ha sido cambiado al plan {PLAN}"
                resp = colorFormatter(resp, "ok")
                print(resp)
                quit(5)
                return
        else:
            resp = colorFormatter("Cancelando...", "info")
            print(resp)
            quit(1)
            return
    else:
        resp = colorFormatter(FAIL, "warning")
        print(resp)
        quit(5)
        return
