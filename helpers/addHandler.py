from helpers.outputDecoder import decoder, check
from helpers.failHandler import failChecker

conditionONT = "ONTID :"
providerMap = {"INTER": 1101, "VNET": 1102, "PUBLICAS": 1104}
vlanProvMap = {"1101": "INTER", "1102": "VNET", "1104": "PUBLICAS"}


def addONU(comm, command, FRAME, SLOT, PORT, SN, NAME, SRV, LP, OLT):
    command(f"interface gpon {FRAME}/{SLOT}")
    command(
        f'ont add {PORT} sn-auth {SN} omci ont-lineprofile-name "{LP}" ont-srvprofile-name "{SRV}"  desc "{NAME}" ') if OLT != "1" else command(
        f'ont add {PORT} sn-auth {SN} omci ont-lineprofile-id {LP} ont-srvprofile-id {SRV}  desc "{NAME}" ')
    value = decoder(comm)
    fail = failChecker(value)
    if fail == None:
        (_, end) = check(value, conditionONT).span()
        ID = value[end: end + 3].replace(" ", "").replace("\n", "")
        if OLT != "1":
            command(
                f"ont optical-alarm-profile {PORT} {ID} profile-name ALARMAS_OPTICAS")
            command(f"ont alarm-policy {PORT} {ID} policy-name FAULT_ALARMS")
        command("quit")
        return (ID, fail)
    else:
        return (None, fail)


def addOnuService(command, comm, SPID, PROVIDER, FRAME, SLOT, PORT, ID, PLAN):
    command("config")
    decoder(comm)
    command(
        f" service-port  {SPID}  vlan  {PROVIDER}  gpon  {FRAME}/{SLOT}/{PORT}  ont {ID}  gemport  14  multi-service  user-vlan  {PROVIDER}  tag-transform  transparent  inbound  traffic-table  name  {PLAN}  outbound  traffic-table  name  {PLAN}"
    )


def addOnuServiceNew(command, comm, SPID, PROVIDER, FRAME, SLOT, PORT, ID, PLAN, GP):
    command("config")
    decoder(comm)
    command(
        f" service-port  {SPID}  vlan  {PROVIDER}  gpon  {FRAME}/{SLOT}/{PORT}  ont {ID}  gemport  {GP}  multi-service  user-vlan  {PROVIDER}  tag-transform  transparent  inbound  traffic-table  index  {PLAN}  outbound  traffic-table  index  {PLAN}"
    )
