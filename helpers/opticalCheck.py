from helpers.outputDecoder import decoder, parser, check
from helpers.failHandler import failChecker

conditionTemp = "Temperature\(C\)                         : "
conditionPwr = "Rx optical power\(dBm\)                  : "


def opticalValues(comm, command, FRAME, SLOT, PORT, ID, show):
    temp = "NA"
    pwr = "NA"
    command(f" interface  gpon  {FRAME}/{SLOT} ")
    command(f" display  ont  optical-info  {PORT}  {ID}  |  no-more")
    command("quit")
    value = decoder(comm)
    fail = failChecker(value)
    command("quit")
    if fail != None:
        if show:
            print(fail)
    else:
        rePwr = check(value, conditionPwr)
        reTemp = check(value, conditionTemp)
        (_, eT) = reTemp.span()
        (_, eP) = rePwr.span()
        pwr = value[eP : eP + 6]
        temp = value[eT : eT + 4].replace("\n", "").replace(" ", "")
    return (temp, pwr)
