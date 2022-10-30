from helpers.outputDecoder import decoder, parser, check
from helpers.failHandler import failChecker
from helpers.getONTSpid import getOntSpid

ip = "IPv4 address               : "
endIp = "Subnet mask"
vlan = "Manage VLAN                : "
planMap = {
    "VLANID":"VLAN ID             : ",
    "PLAN": "Inbound table name  : "
}

def preWan(comm, command, SLOT, PORT, ID):
    command(f"interface gpon 0/{SLOT}")
    command(f"display ont wan-info {PORT} {ID}")
    (value, re) = parser(comm, vlan, "s")
    fail = failChecker(value)
    if fail == None:
        (_, e) = re.span()
        vUsed = value[e : e + 4]
        print(f"Al ONT se le ha agregado la vlan {vUsed}")
        return vUsed
    else:
        print(fail)
        return fail


def wan(comm, command, SLOT, PORT, ID):
    IPADDRESS = ""
    SPID = "NA"
    PLAN = "NA"
    VLAN = "NA"
    result = getOntSpid(comm,command,SLOT,PORT,ID)
    if(result["values"] == None):
        return ("NA", "NA", "NA", "NA")
    if(result["ttl"] == 1):
        SPID = result["values"]
        command(f" display  service-port  {SPID}")
        value = decoder(comm)
        fail = failChecker(value)
        if(fail == None):
            (_,sV) = check(value,planMap["VLANID"]).span()
            (_,sP) = check(value,planMap["PLAN"]).span()
            VLAN = value[sV:sV+4]
            PLAN = value[sP:sP+10].replace(" ", "").replace("\n", "")
            command(f"display ont wan-info 0 {SLOT} {PORT} {ID}")
            val = decoder(comm)
            failIp = failChecker(val)
            if(failIp == None):
                (_,s) = check(val,ip).span()
                (e,_) = check(val,endIp).span()
                IPADDRESS = value[s : e -1].replace(" ", "").replace("\n", "")
            return (VLAN,PLAN,IPADDRESS,SPID)
        else:
            return ("NA", "NA", "NA","NA")
    elif(result["ttl"] > 1):
        value = decoder(comm)
        fail = failChecker(value)
        SPID = result["values"][0]
        command(f"display service-port {SPID}")
        if(fail == None):
            (_,sV1) = check(value,planMap["VLANID"]).span()
            (_,sP1) = check(value,planMap["PLAN"]).span()
            VLAN = value[sV1:sV1+4]
            PLAN = value[sP1:sP1+10].replace(" ", "").replace("\n", "")
        command(f"display ont wan-info 0 {SLOT} {PORT} {ID}")
        val = decoder(comm)
        failIp = failChecker(val)
        if(failIp == None):
            (_,s) = check(val,ip).span()
            (e,_) = check(val,endIp).span()
            IPADDRESS = value[s : e -1].replace(" ", "").replace("\n", "")
        return (VLAN,PLAN,IPADDRESS,SPID)
