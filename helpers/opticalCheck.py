from helpers.outputDecoder import decoder, parser, check
from helpers.failHandler import failChecker
from helpers.printer import log

conditionTemp = "Temperature\(C\)                         : "
conditionPwr = "Rx optical power\(dBm\)                  : "


def opticalValues(comm, command, FRAME, SLOT, PORT, ID, show):
    TEMP = None
    PWR = None
    command(f"  interface  gpon  {FRAME}/{SLOT}  ")
    command(f"  display  ont  optical-info  {PORT}  {ID}  |  no-more")
    command("quit")
    value = decoder(comm)
    fail = failChecker(value)
    if fail != None:
        if show:
            log(fail)
    else:
        rePwr = check(value, conditionPwr)
        reTemp = check(value, conditionTemp)
        (_, eT) = reTemp.span()
        (_, eP) = rePwr.span()
        PWR = value[eP : eP + 6]
        TEMP = value[eT : eT + 4].replace("\n", "").replace(" ", "")
    return (TEMP, PWR)
