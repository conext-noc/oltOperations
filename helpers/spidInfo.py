from helpers.outputDecoder import parser

conditionSPID = """Next valid free service virtual port ID: """
conditionSpidCheck = "-------------------------------------------------------------"


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
    if re != None:
        (s, _) = re[0]
        (_, e) = re[1]
        print(value[s:e])
    else:
        spid = getSPID(comm, command, enter)
        print(f"No se agrego el SPID, el SPID libre es {spid}")
