from helpers.getONTSpid import getSPIDChange
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
        NAME = input("Ingrese el nombre del cliente : ").upper()

    result = getSPIDChange(comm, command, SLOT, PORT, ID)
    if(result["values"] != None):
        if result["ttl"] == 1:
            spid = result["values"]
            command(f"display service-port {spid}")
            value = decoder(comm)
            fail = failChecker(value)
            if(fail == None):
                (_,sV) = check(value,planMap["VLANID"]).span()
                (_,sP) = check(value,planMap["PLAN"]).span()
                vlan = value[sV:sV+4]
                plan = value[sP:sP+10].replace(" ", "").replace("\n", "")
                print(f"""
    NOMBRE DE CLIENTE   :   {NAME}
    VLAN DE CLIENTE     :   {vlan}
    PLAN DE CLIENTE     :   {plan}
    """)
                PROVIDER = input("Ingrese el nuevo proveedor de cliente [INTER | VNET] : ").upper()
                PLAN = input("Ingrese plan de cliente : ").upper()
                prov = providerMap[PROVIDER]
                command(f" undo  service-port  {spid}")
                command(
                    f"service-port {spid} vlan {prov} gpon {FRAME}/{SLOT}/{PORT} ont {ID} gemport 14 multi-service user-vlan {prov} tag-transform transparent inbound traffic-table name {PLAN} outbound traffic-table name {PLAN}"
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
            else:
                print(fail)
                return
        else:
            print(f"""
    NOMBRE DE CLIENTE   :   {NAME}""")
            value1 = decoder(comm)
            fail1 = failChecker(value1)
            spid1 = result["values"][0]
            spid2 = result["values"][1]
            command(f"display service-port {spid1}")
            if(fail1 == None):
                (_,sV1) = check(value1,planMap["VLANID"]).span()
                (_,sP1) = check(value1,planMap["PLAN"]).span()
                vlan1 = value1[sV1:sV1+4]
                plan1 = value1[sP1:sP1+10].replace(" ", "").replace("\n", "")
                print(f"""
    VLAN - 1 DE CLIENTE :   {vlan1}
    PLAN - 1 DE CLIENTE :   {plan1}
    """)
            else:
                print(f"El Service Port ID {spid1} tiene error o no existe : {fail1}")
            value2 = decoder(comm)
            fail2 = failChecker(value2)
            command(f"display service-port {spid2}")
            if(fail2 == None):
                (_,sV2) = check(value2,planMap["VLANID"]).span()
                (_,sP2) = check(value2,planMap["PLAN"]).span()
                vlan2 = value2[sV2:sV2+4]
                plan2 = value2[sP2:sP2+10].replace(" ", "").replace("\n", "")
                print(f"""
    VLAN - 2 DE CLIENTE :   {vlan2}
    PLAN - 2 DE CLIENTE :   {plan2}
    """)
            else:
                print(f"El Service Port ID {spid2} tiene error o no existe : {fail2}")
                return
            PROVIDER = input("Ingrese el nuevo proveedor de cliente [INTER | VNET] : ").upper()
            PLAN = input("Ingrese plan de cliente : ").upper()
            prov = providerMap[PROVIDER]
            command(f" undo  service-port  {spid1}")
            command(f" undo  service-port  {spid2}")
            command(
                f"service-PORT {spid1} vlan {prov} gpon {FRAME}/{SLOT}/{PORT} ont {ID} gemport 14 multi-service user-vlan {prov} tag-transform transparent inbound traffic-table name {PLAN} outbound traffic-table name {PLAN}"
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
    else:
        print(result["ttl"])