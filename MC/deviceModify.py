from helpers.getWanData import wan
from helpers.serialLookup import serialSearch
from helpers.getONTSpid import getOntSpid

providerMap = {"INTER": 1101, "VNET": 1102, "PUBLICAS": 1104}

planMap = {
    "VLANID":"VLAN ID             : ",
    "PLAN": "Inbound table name  : "
}

def deviceModify(comm, command, OLT):
    FRAME = ""
    SLOT = ""
    PORT = ""
    ID = ""
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
    if(lookupType == "S"):
        SN = input("Ingrese el Serial del Cliente a buscar : ")
        (FRAME,SLOT,PORT,ID,NAME,STATE) = serialSearch(comm,command,SN)
    if(lookupType == "D"):
        FRAME = input("Ingrese frame de cliente : ")
        SLOT = input("Ingrese slot de cliente : ")
        PORT = input("Ingrese puerto de cliente : ")
        ID = input("Ingrese el id del cliente : ")
        ## SEARCH FOR NAME IN OLT!!
    command(f"interface gpon {FRAME}/{SLOT}")
    if action == "CT":
        NAME = input("Ingrese el nuevo nombre del cliente : ")
        command(f"ont modify {PORT} {ID} desc {NAME}")
        print(
            f"Al Cliente {FRAME}/{SLOT}/{PORT}/{ID} OLT {OLT} se ha cambiado de titular a {NAME}"
        )
        return
    if action == "CO":
        SN = input("Ingrese el nuevo ont del cliente : ")
        command(f"ont modify {PORT} {ID} sn {SN}")
        print(
            f"Al Cliente 0/{SLOT}/{PORT}/{ID} OLT {OLT} se ha sido cambiado el ont a {SN}"
        )
    if action == "CV":
        (VLAN,PLAN,IPADDRESS,SPID) = wan(comm, command, SLOT, PORT, ID)
        print(f"""
        NOMBRE DE CLIENTE   :   {NAME}
        VLAN DE CLIENTE     :   {VLAN}
        PLAN DE CLIENTE     :   {PLAN}
        IP DEL CLIENTE      :   {IPADDRESS}
        SPID                :   {SPID}
        """)
        PROVIDER = input("Ingrese el nuevo proveedor de cliente [INTER | VNET] : ").upper()
        PLAN = input("Ingrese plan de cliente : ").upper()
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
        print(
            f"El Cliente {NAME} {FRAME}/{SLOT}/{PORT}/{ID} OLT {OLT} ha sido cambiado al proveedor {PROVIDER}"
        )
        return
    if action == "CP":
        PLAN = input("Ingrese el nuevo plan de cliente : ")
        result = getOntSpid(comm, command, SLOT, PORT, ID)
        if (result["ttl"] == 2):
            spid1 = result["values"][0]
            spid2 = result["values"][1]
            command(
                f"service-port {spid1} inbound traffic-table name {PLAN} outbound traffic-table name {PLAN}")
            command(
                f"service-port {spid2} inbound traffic-table name {PLAN} outbound traffic-table name {PLAN}")
        if (result["ttl"] == 1):
            spid = result["values"]
            command(
                f"service-port {spid} inbound traffic-table name {PLAN} outbound traffic-table name {PLAN}")
        print(
            f"El Cliente {NAME} {FRAME}/{SLOT}/{PORT}/{ID} OLT {OLT} ha sido cambiado al plan {PLAN}")
        return
