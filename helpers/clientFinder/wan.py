from time import sleep
from helpers.utils.decoder import decoder, check
from helpers.failHandler.fail import failChecker
from helpers.operations.spid import ontSpid
from helpers.info.plans import planX15Maps, planX2Maps, planX15NMaps
from helpers.utils.printer import colorFormatter, log
from helpers.info.regexConditions import wanMapper

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
        command(f"display ont wan-info {FRAME}/{SLOT} {PORT} {ID} | exclude IPv6 | exclude Prefix | exclude DS | exclude NAT | exclude type | exclude Default | exclude DNS | exclude 60 | exclude mask")
        sleep(3)
        value = decoder(comm)
        fail = failChecker(value)
        regexIp = check(value, ip)
        regexVl = check(value, vlan)
        if (fail == None and regexIp != None and regexVl != None):
            (_, sIp) = regexIp.span()
            (eIp, s) = regexVl.span()
            activeVlan = int(value[s:s+4])
            IPADDRESS = value[sIp: eIp - 1].replace(" ", "").replace("\n", "")
        for wanData in result:
            plan = planMap[str(wanData["RX"])]
            STATE = "used" if wanData["ID"] == activeVlan else wanData["STATE"] if activeVlan == None else "not used"
            prov = wanMapper[OLT][f"{wanData['ID']}"]
            WAN.append(
                {"vlan": wanData["ID"], "spid": wanData["SPID"], "state": STATE, "plan_name": f"{plan}_{prov}"})
        return (IPADDRESS, WAN)
    else:
        FAIL = failSpid
        log(colorFormatter(FAIL, "info"))
        return (IPADDRESS, [{"spid": None, "vlan": None, "plan": None, "plan_name": None, "state": None}])
