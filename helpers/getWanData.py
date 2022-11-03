from helpers.outputDecoder import decoder, parser, check
from helpers.failHandler import failChecker
from helpers.spidHandler import ontSpid, planX15Maps, planX2Maps

ip = "IPv4 address               : "
endIp = "Subnet mask"
vlan = "Manage VLAN                : "
planMap = {"VLANID": "VLAN ID             : ", "PLAN": "Inbound table name  : "}


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


def wan(comm, command, FRAME, SLOT, PORT, ID, OLT):
    IPADDRESS = None
    FAIL = None
    WAN = []
    planMap = planX15Maps if OLT == "15" else planX2Maps
    (result, failSpid) = ontSpid(comm, command, FRAME, SLOT, PORT, ID)
    if failSpid == None:
        print(result)
        for wanData in result:
            plan = planMap[str(wanData["RX"])]
            WAN.append({"VLAN": wanData["ID"], "SPID": wanData["SPID"], "PLAN": plan, "STATE": wanData["STATE"]})
        command(f" display  ont  wan-info  {FRAME}/{SLOT}  {PORT}  {ID}")
        val = decoder(comm)
        failIp = failChecker(val)
        if failIp == None:
            (_, s) = check(val, ip).span()
            (e, _) = check(val, endIp).span()
            IPADDRESS = val[s : e - 1].replace(" ", "").replace("\n", "")
        return (IPADDRESS, WAN, FAIL)
    else:
        FAIL = failSpid
        return (IPADDRESS, WAN, FAIL)
