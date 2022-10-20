from helpers.outputDecoder import parser, check
from verifyReset.verifyReset import verifyWAN
from helpers.failHandler import failChecker

conditionONT = """ONTID :"""
conditionFail = "Failure: "
providerMap = {"INTER": 1101, "VNET": 1102, "PUBLICAS": 1104}


def addONU(comm, command, enter, SLOT, PORT, SN, NAME, SRV, LP):
    command(f"interface gpon 0/{SLOT}")
    enter()
    command(
        f'ont add {PORT} sn-auth {SN} omci ont-lineprofile-name "{LP}" ont-srvprofile-name "{SRV}"  desc "{NAME}" '
    )
    enter()
    (value, re) = parser(comm, conditionONT, "s")
    fail = failChecker(value)
    if fail == None:
        print(fail)
    else:
        end = re.span()[1]
        ID = value[end : end + 3].replace(" ", "")
        command(f"ont optical-alarm-profile {PORT} {ID} profile-id 3")
        enter()
        command(f"ont alarm-policy {PORT} {ID} policy-id 1")
        enter()
        preg = input(
            "Desea verificar si el cliente ya tiene la wan interface configurada? [Y | N] : "
        )
        if preg == "Y":
            verifyWAN(comm, command, enter, SLOT, PORT, ID)
        Prov= input("Ingrese proevedor de cliente [INTER | VNET | PUBLICAS] : ")
        PROVIDER = providerMap[Prov]
        addVlan = input("Se agregara vlan al puerto? (es bridge) [Y/N] : ")
        if addVlan == "Y":
            command(f"ont port native-vlan {PORT} {ID} eth 1 vlan {PROVIDER}")
            enter()
        command("quit")
        enter()
        return (ID,PROVIDER)


def addOnuService(command, enter, SPID, PROVIDER, SLOT, PORT, ID, PLAN):
    command(
        f"""service-PORT {SPID} vlan {PROVIDER} gpon 0/{SLOT}/{PORT} ont {ID} gemport 14 multi-service user-vlan {PROVIDER} tag-transform transparent inbound traffic-table name {PLAN} outbound traffic-table name {PLAN}"""
    )
    enter()
