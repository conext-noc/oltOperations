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

def wan(comm, command, client):
    IPADDRESS = None
    FAIL = None
    WAN = []
    activeVlan = None
    planMap = planX15Maps if client["olt"] == "2" else planX2Maps if client["olt"] == "3" else planX15NMaps
    (result, failSpid) = ontSpid(comm, command, client)
    if failSpid == None:
        command(f"display ont wan-info {client['frame']}/{client['slot']} {client['port']} {client['onu_id']} | exclude IPv6 | exclude Prefix | exclude DS | exclude NAT | exclude type | exclude Default | exclude DNS | exclude 60 | exclude mask")
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
            prov = wanMapper[client["olt"]][f"{wanData['ID']}"]
            PROVIDER = "INTER" if prov == "1" else "2" if prov == "2" else "PUBLICAS"
            WAN.append(
                {"vlan": wanData["ID"], "spid": wanData["SPID"], "state": STATE, "plan_name": f"{plan}_{prov}", "provider": PROVIDER})
        return (IPADDRESS, WAN)
    else:
        FAIL = failSpid
        log(colorFormatter(FAIL, "info"))
        return (IPADDRESS, [{"spid": None, "vlan": None, "plan": None, "plan_name": None, "state": None}])
