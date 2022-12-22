from helpers.utils.decoder import decoder, check
from helpers.failHandler.fail import failChecker
from helpers.operations.spid import ontSpid
from helpers.info.plans import planX15Maps,planX2Maps,planX15NMaps
from helpers.utils.printer import colorFormatter, log

ip = "IPv4 address               : "
endIp = "Subnet mask"
vlan = "Manage VLAN                : "
planMap = {"VLANID": "VLAN ID             : ",
           "PLAN": "Inbound table name  : "}

def wan(comm, command, FRAME, SLOT, PORT, ID, OLT):
    IPADDRESS = None
    FAIL = None
    WAN = []
    activeVlan = None
    planMap = planX15Maps if OLT == "2" else planX2Maps if OLT == "3" else planX15NMaps
    (result, failSpid) = ontSpid(comm, command, FRAME, SLOT, PORT, ID)
    if failSpid == None:
        command(f"display ont wan-info {FRAME}/{SLOT} {PORT} {ID} | exclude IPv6 | exclude Prefix | exclude DS | exclude NAT | exclude type | exclude address | exclude Default | exclude DNS | exclude 60 | exclude mask")
        command("q")
        value = decoder(comm)
        fail = failChecker(value)
        data = check(value, "IPv4 Connection status     : Connected")
        if (data != None and fail == None):
            (_, s) = data.span()
            activeVlan = int(value[s+33:s+37])
        for wanData in result:
            plan = planMap[str(wanData["RX"])]
            STATE = wanData["STATE"] if activeVlan == None else (
                "used" if wanData["ID"] == activeVlan else "not used")
            WAN.append(
                {"vlan": wanData["ID"], "spid": wanData["SPID"], "plan": plan, "state": STATE})
        command(f" display  ont  wan-info  {FRAME}/{SLOT}  {PORT}  {ID}")
        val = decoder(comm)
        failIp = failChecker(val)
        if failIp == None:
            (_, s) = check(val, ip).span()
            (e, _) = check(val, endIp).span()
            IPADDRESS = val[s: e - 1].replace(" ", "").replace("\n", "")
        else:
            IPADDRESS = failIp
        return (IPADDRESS, WAN)
    else:
        FAIL = failSpid
        log(colorFormatter(FAIL, "info"))
        return (IPADDRESS, [{"spid":None, "vlan": None, "plan": None}])
