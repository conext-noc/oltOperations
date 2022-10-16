from helpers.outputDecoder import parser
from helpers.failHandler import failChecker

conditionSPID = """Next valid free service virtual port ID: """
conditionSpidCheck = "-------------------------------------------------------------"
conditionSPIDChckO = (
    "-----------------------------------------------------------------------------"
)


def getSPID(comm, command, enter):
    command("display service-port next-free-index")
    enter()
    enter()
    (value, re) = parser(comm, conditionSPID, "s")
    end = re.span()[1]
    spid = value[end : end + 4]
    return spid


def verifySPID(comm, command, enter, spid):
    command(f"display service-port {spid} | no-more")
    enter()
    (value, re) = parser(comm, conditionSpidCheck, "m")
    fail = failChecker(value)
    if fail == None:
        (s, _) = re[0]
        (_, e) = re[1]
        print(value[s:e])
    else:
        print(fail)
        spid = getSPID(comm, command, enter)
        print(f"No se agrego el SPID, el siguiente SPID libre es {spid}")


def clientSPID(comm, command, enter, SLOT, PORT, ID):
    command(f"display service-port port 0/{SLOT}/{PORT} ont {ID}")
    enter()
    (value, _) = parser(comm, conditionSPIDChckO, "m")
    fail = failChecker(value)
    if fail == None:
        print(value)

    else:
        print(fail)
        return None
