from helpers.getONTSpid import getSPIDChange
from helpers.outputDecoder import decoder, parser, checkIter, check
from helpers.serialLookup import serialSearch
from helpers.ontCheck import verifyValues
from helpers.failHandler import failChecker
from verifyReset.verifyReset import verifyWAN
from time import sleep

planMap = {
    "VLANID":"VLAN ID             : ",
    "PLAN": "Inbound table name  : "
}

existingCond = (
    "-----------------------------------------------------------------------------"
)
newCond = "----------------------------------------------------------------------------"
newCondFSP = "F/S/P               : "
newCondSn = "Ont SN              : "
existing = {
    "CF": "Control flag            : ",
    "RE": "Run state               : ",
    "DESC": "Description             : ",
    "LDC": "Last down cause         : ",
}


def newLookup(comm, command, olt):
    client = []
    command("display ont autofind all | no-more")
    sleep(5)
    (value, regex) = parser(comm, newCond, "m")
    for ont in range(len(regex) - 1):
        (_, s) = regex[ont]
        (e, _) = regex[ont + 1]
        result = value[s:e]
        (_, eFSP) = check(result, newCondFSP).span()
        (_, eSN) = check(result, newCondSn).span()
        aSN = result[eSN : eSN + 16].replace("\n", "").replace(" ", "")
        aFSP = result[eFSP : eFSP + 6].replace("\n", "").replace(" ", "")
        client.append({"FSP": aFSP, "SN": aSN, "IDX": ont})
    print("| {:^3} | {:^6} | {:^16} |".format("IDX", "F/S/P", "SN"))
    for ont in client:
        FSP = ont["FSP"].replace(" ", "")
        SN = ont["SN"].replace(" ", "")
        IDX = ont["IDX"] + 1
        print("| {:^3} | {:^6} | {:^16} |".format(IDX, FSP, SN))


def existingLookup(comm, command, olt):
    FRAME = ""
    SLOT = ""
    PORT = ""
    ID = ""
    NAME = ""
    STATE = ""
    SPID = "NA"
    SPID1 = "NA"
    SPID2 = "NA"
    VLAN = "NA"
    PLAN = "NA"
    VLAN1 = "NA"
    PLAN1 = "NA"
    VLAN2 = "NA"
    PLAN2 = "NA"
    lookupType = input("Buscar cliente por serial, por nombre o por F/S/P/ID [S | N | F] : ")
    if lookupType == "S":
        SN = input("Ingrese el Serial del Cliente a buscar : ")
        command(f"display ont info by-sn {SN} | no-more")
        sleep(3)
        (FRAME,SLOT,PORT,ID,NAME,STATE) = serialSearch(comm,command,SN)
        (temp, pwr) = verifyValues(comm, command, SLOT, PORT, ID)
        result = getSPIDChange(comm, command, SLOT, PORT, ID)
        if(result["values"] != None):
            if result["ttl"] == 1:
                SPID = result["values"]
                command(f"display service-port {SPID}")
                value = decoder(comm)
                fail = failChecker(value)
                if(fail == None):
                    (_,sV) = check(value,planMap["VLANID"]).span()
                    (_,sP) = check(value,planMap["PLAN"]).span()
                    VLAN = value[sV:sV+4]
                    PLAN = value[sP:sP+10].replace(" ", "").replace("\n", "")
                print(
                f"""
    FRAME               :   {FRAME}
    SLOT                :   {SLOT}
    PORT                :   {PORT}
    ID                  :   {ID}
    NAME                :   {NAME}
    STATE               :   {STATE}
    VLAN                :   {VLAN}
    PLAN                :   {PLAN}
    SPID                :   {SPID}
    TEMPERATURA         :   {temp}
    POTENCIA            :   {pwr}
    """)
            else:
                value1 = decoder(comm)
                fail1 = failChecker(value1)
                SPID1 = result["values"][0]
                SPID2 = result["values"][1]
                command(f"display service-port {SPID1}")
                if(fail1 == None):
                    (_,sV1) = check(value1,planMap["VLANID"]).span()
                    (_,sP1) = check(value1,planMap["PLAN"]).span()
                    VLAN1 = value1[sV1:sV1+4]
                    PLAN1 = value1[sP1:sP1+10].replace(" ", "").replace("\n", "")
                value2 = decoder(comm)
                fail2 = failChecker(value2)
                command(f"display service-port {SPID2}")
                if(fail2 == None):
                    (_,sV2) = check(value2,planMap["VLANID"]).span()
                    (_,sP2) = check(value2,planMap["PLAN"]).span()
                    VLAN2 = value2[sV2:sV2+4]
                    PLAN2 = value2[sP2:sP2+10].replace(" ", "").replace("\n", "")
                print(
            f"""
FRAME               :   {FRAME}
SLOT                :   {SLOT}
PORT                :   {PORT}
ID                  :   {ID}
NAME                :   {NAME}
STATE               :   {STATE}
VLAN1               :   {VLAN1}
PLAN1               :   {PLAN1}
SPID1               :   {SPID1}
VLAN2               :   {VLAN2}
PLAN2               :   {PLAN2}
SPID2               :   {SPID2}
TEMPERATURA         :   {temp}
POTENCIA            :   {pwr}
""")

    elif lookupType == "F":
        FRAME = input("Ingrese frame de cliente : ")
        SLOT = input("Ingrese slot de cliente : ")
        PORT = input("Ingrese puerto de cliente : ")
        ID = input("Ingrese el id del cliente : ")
        command(f"display ont info {FRAME} {SLOT} {PORT} {ID} | no-more")
        sleep(3)
        (val, regex) = parser(comm, existingCond, "m")
        (_, s) = regex[0]
        (e, _) = regex[len(regex) - 1]
        value = val[s:e]
        (_, sDESC) = check(value, existing["DESC"]).span()
        (_, sCF) = check(value, existing["CF"]).span()
        (eCF, _) = check(value, existing["RE"]).span()
        (eDESC, _) = check(value, existing["LDC"]).span()
        NAME = value[sDESC:eDESC].replace("\n", "")
        STATE = value[sCF:eCF].replace("\n", "")
        (temp, pwr) = verifyValues(comm, command, SLOT, PORT, ID)
        result = getSPIDChange(comm, command, SLOT, PORT, ID)
        if(result["values"] != None):
            if result["ttl"] == 1:
                SPID = result["values"]
                command(f"display service-port {SPID}")
                value = decoder(comm)
                fail = failChecker(value)
                if(fail == None):
                    (_,sV) = check(value,planMap["VLANID"]).span()
                    (_,sP) = check(value,planMap["PLAN"]).span()
                    VLAN = value[sV:sV+4]
                    PLAN = value[sP:sP+10].replace(" ", "").replace("\n", "")
                print(
                f"""
    FRAME               :   {FRAME}
    SLOT                :   {SLOT}
    PORT                :   {PORT}
    ID                  :   {ID}
    NAME                :   {NAME}
    STATE               :   {STATE}
    VLAN                :   {VLAN}
    PLAN                :   {PLAN}
    SPID                :   {SPID}
    TEMPERATURA         :   {temp}
    POTENCIA            :   {pwr}
    """)
            else:
                value1 = decoder(comm)
                fail1 = failChecker(value1)
                SPID1 = result["values"][0]
                SPID2 = result["values"][1]
                command(f"display service-port {SPID1}")
                if(fail1 == None):
                    (_,sV1) = check(value1,planMap["VLANID"]).span()
                    (_,sP1) = check(value1,planMap["PLAN"]).span()
                    VLAN1 = value1[sV1:sV1+4]
                    PLAN1 = value1[sP1:sP1+10].replace(" ", "").replace("\n", "")
                value2 = decoder(comm)
                fail2 = failChecker(value2)
                command(f"display service-port {SPID2}")
                if(fail2 == None):
                    (_,sV2) = check(value2,planMap["VLANID"]).span()
                    (_,sP2) = check(value2,planMap["PLAN"]).span()
                    VLAN2 = value2[sV2:sV2+4]
                    PLAN2 = value2[sP2:sP2+10].replace(" ", "").replace("\n", "")
                print(
            f"""
FRAME               :   {FRAME}
SLOT                :   {SLOT}
PORT                :   {PORT}
ID                  :   {ID}
NAME                :   {NAME}
STATE               :   {STATE}
VLAN1               :   {VLAN1}
PLAN1               :   {PLAN1}
SPID1               :   {SPID1}
VLAN2               :   {VLAN2}
PLAN2               :   {PLAN2}
SPID2               :   {SPID2}
TEMPERATURA         :   {temp}
POTENCIA            :   {pwr}
""")

    elif lookupType == "N":
        NAME = input("Ingrese el Nombre del Cliente a buscar : ")
        command(f'display ont info by-desc "{NAME}" | no-more')
        sleep(3)
        (value, regex) = parser(comm, existingCond, "m")
        (_, s) = regex[0]
        (e, _) = regex[len(regex) - 1]
        print(value[s:e])
    
    else:
        print(f'la opcion "{lookupType}" no existe')
