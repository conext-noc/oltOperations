from helpers.getONTSpid import getOntSpid
from helpers.getWanData import wan
from helpers.serialLookup import serialSearch
from helpers.outputDecoder import  check, decoder
from helpers.failHandler import failChecker

providerMap = {"INTER": 1101, "VNET": 1102, "PUBLICAS": 1104}

planMap = {
    "VLANID":"VLAN ID             : ",
    "PLAN": "Inbound table name  : "
}

def providerChange(comm, command, olt):
    FRAME = ""
    SLOT = ""
    PORT = ""
    ID = ""
    NAME = ""
    lookupType = input("Buscar cliente por serial o por F/S/P [S | F] : ").upper()
    if (lookupType == "S"):
        SN = input("Ingrese el Serial del Cliente a buscar : ")
        (FRAME,SLOT,PORT,ID,NAME,STATE) = serialSearch(comm,command,SN)
    if(lookupType == "F"):
        FRAME = input("Ingrese frame de cliente : ") 
        SLOT = input("Ingrese slot de cliente : ")
        PORT = input("Ingrese puerto de cliente : ")
        ID = input("Ingrese el id del cliente : ")
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
            f"El Cliente {NAME} {FRAME}/{SLOT}/{PORT}/{ID} OLT {olt} ha sido cambiado al proveedor {PROVIDER}"
        )
    return