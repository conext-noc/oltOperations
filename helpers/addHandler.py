from helpers.outputDecoder import parser
from helpers.getWanData import preWan
from helpers.failHandler import failChecker

conditionONT = """ONTID :"""
conditionFail = "Failure: "
providerMap = {"INTER": 1101, "VNET": 1102, "PUBLICAS": 1104}
vlanProvMap = {"1101": "INTER", "1102": "VNET", "1104": "PUBLICAS"}


def addONU(comm, command, FRAME, SLOT, PORT, SN, NAME, SRV, LP):
    command(f"interface gpon {FRAME}/{SLOT}")
    command(
        f'ont add {PORT} sn-auth {SN} omci ont-lineprofile-name "{LP}" ont-srvprofile-name "{SRV}"  desc "{NAME}" '
    )
    (value, re) = parser(comm, conditionONT, "s")
    fail = failChecker(value)
    if fail != None:
        print(fail)
    else:
        end = re.span()[1]
        ID = value[end : end + 3].replace(" ", "").replace("\n", "")
        command(f"ont optical-alarm-profile {PORT} {ID} profile-name ALARMAS_OPTICAS")
        command(f"ont alarm-policy {PORT} {ID} policy-name FAULT_ALARMS")
        preg = input(
            "Desea verificar si el cliente ya tiene la wan interface configurada? [Y | N] : "
        ).upper()
        if preg == "Y":
            preWan(comm, command, SLOT, PORT, ID)
        Prov = input(
            "Ingrese proevedor de cliente [INTER | VNET | PUBLICAS] : "
        ).upper()
        PROVIDER = providerMap[Prov]
        addVlan = input("Se agregara vlan al puerto? (es bridge) [Y/N] : ").upper()
        if addVlan == "Y":
            command(f"ont port native-vlan {PORT} {ID} eth 1 vlan {PROVIDER}")
        command("quit")
        return (ID, vlanProvMap[f"{str(PROVIDER)}"])


def addOnuService(command, SPID, PROVIDER, FRAME, SLOT, PORT, ID, PLAN):
    command("config")
    command(
        f" service-port  {SPID}  vlan  {PROVIDER}  gpon  {FRAME}/{SLOT}/{PORT}  ont {ID}  gemport  14  multi-service  user-vlan  {PROVIDER}  tag-transform  transparent  inbound  traffic-table  name  {PLAN}  outbound  traffic-table  name  {PLAN}"
    )
