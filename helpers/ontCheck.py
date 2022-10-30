from helpers.outputDecoder import decoder, parser, check
from helpers.failHandler import failChecker

conditionTemp = "Temperature\(C\)                         : "
conditionPwr = "Rx optical power\(dBm\)                  : "


def verifyValues(comm, command, SLOT, PORT, ID, show):
    decoder(comm)
    command(f"interface gpon 0/{SLOT}")
    command(f"display ont optical-info {PORT} {ID} | no-more")
    command("quit")
    (value, rePwr) = parser(comm, conditionPwr, "s")
    fail = failChecker(value)
    command("quit")

    if fail != None:
        if(show):
            print(fail)
            return fail
        return fail
        

    else:
        reTemp = check(value, conditionTemp)
        (_, eT) = reTemp.span()
        (_, eP) = rePwr.span()
        pwr = value[eP: eP + 6]
        temp = value[eT: eT + 4].replace("\n", "").replace(" ", "")
        return (temp, pwr)