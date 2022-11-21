from helpers.outputDecoder import decoder, parser, check
from helpers.failHandler import failChecker
from helpers.spidHandler import ontSpid, planX15Maps, planX2Maps
from helpers.formatter import colorFormatter

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
    activeVlan = None
    planMap = planX15Maps if OLT == "15" else planX2Maps
    (result, failSpid) = ontSpid(comm, command, FRAME, SLOT, PORT, ID)
    if failSpid == None:
        command(f"display ont wan-info {FRAME}/{SLOT} {PORT} {ID} | exclude IPv6 | exclude Prefix | exclude DS | exclude NAT | exclude type | exclude address | exclude Default | exclude DNS | exclude 60 | exclude mask")
        value = decoder(comm)
        fail = failChecker(value)
        data = check(value, "IPv4 Connection status     : Connected")
        if(data != None and fail == None):
            (_,s) = data.span()
            activeVlan = int(value[s+33:s+37])
        for wanData in result:
            plan = planMap[str(wanData["RX"])]
            STATE = wanData["STATE"] if activeVlan == None else ("used" if wanData["ID"] == activeVlan else "not used")
            WAN.append({"VLAN": wanData["ID"], "SPID": wanData["SPID"], "PLAN": plan, "STATE": STATE})
        command(f" display  ont  wan-info  {FRAME}/{SLOT}  {PORT}  {ID}")
        val = decoder(comm)
        failIp = failChecker(val)
        if failIp == None:
            (_, s) = check(val, ip).span()
            (e, _) = check(val, endIp).span()
            IPADDRESS = val[s : e - 1].replace(" ", "").replace("\n", "")
        return (IPADDRESS, WAN)
    else:
        FAIL = failSpid
        print(colorFormatter(FAIL, "info"))
        return (IPADDRESS, WAN)
