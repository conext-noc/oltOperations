from helpers.outputDecoder import decoder, parser, check
from helpers.failHandler import failChecker

conditionTemp = "Temperature\(C\)                         : "
conditionPwr = "Rx optical power\(dBm\)                  : "


def verifyValues(comm, command, enter, SLOT, PORT, ID):
    enter()
    decoder(comm)
    command(f"interface gpon 0/{SLOT}")
    enter()

    command(f"display ont optical-info {PORT} {ID} | no-more")
    enter()
    (value, rePwr) = parser(comm, conditionPwr, "s")
    reTemp = check(value, conditionTemp)
    fail = failChecker(value)
    if fail == None:
        print(fail)
        command("quit")
        enter()
    else:
        command("quit")
        enter()
        (_, eT) = reTemp.span()
        (_, eP) = rePwr.span()
        pwr = value[eP : eP + 6]
        temp = value[eT : eT + 4]
        return (temp, pwr)
