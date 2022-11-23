from helpers.outputDecoder import parser, decoder, check
from helpers.getWanData import preWan
from helpers.failHandler import failChecker

conditionONT = "ONTID :"
providerMap = {"INTER": 1101, "VNET": 1102, "PUBLICAS": 1104}
vlanProvMap = {"1101": "INTER", "1102": "VNET", "1104": "PUBLICAS"}


def addONU(comm, command, FRAME, SLOT, PORT, SN, NAME, SRV, LP):
    command(f"interface gpon {FRAME}/{SLOT}")
    command(f'ont add {PORT} sn-auth {SN} omci ont-lineprofile-name "{LP}" ont-srvprofile-name "{SRV}"  desc "{NAME}" ')
    value = decoder(comm)
    fail = failChecker(value)
    if fail != None:
        return (None, None, fail)
    else:
        (_, end) = check(value, conditionONT).span()
        ID = value[end : end + 3].replace(" ", "").replace("\n", "")
        command(f"ont optical-alarm-profile {PORT} {ID} profile-name ALARMAS_OPTICAS")
        command(f"ont alarm-policy {PORT} {ID} policy-name FAULT_ALARMS")
        command("quit")
        return (ID, fail)


def addOnuService(command, comm, SPID, PROVIDER, FRAME, SLOT, PORT, ID, PLAN):
    command("config")
    decoder(comm)
    command(
        f" service-port  {SPID}  vlan  {PROVIDER}  gpon  {FRAME}/{SLOT}/{PORT}  ont {ID}  gemport  14  multi-service  user-vlan  {PROVIDER}  tag-transform  transparent  inbound  traffic-table  name  {PLAN}  outbound  traffic-table  name  {PLAN}"
    )
