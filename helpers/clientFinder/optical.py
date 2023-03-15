from time import sleep
from helpers.utils.decoder import decoder, check
from helpers.failHandler.fail import failChecker
from helpers.utils.printer import log

conditionTemp = "Temperature\(C\)                         : "
conditionPwr = "Rx optical power\(dBm\)                  : "


def opticalValues(comm, command, data, show):
    value = decoder(comm)
    TEMP = None
    PWR = None
    command(f'  interface  gpon  {data["frame"]}/{data["slot"]}  ')
    sleep(2)
    command(f'  display  ont  optical-info  {data["port"]}  {data["onu_id"]}  |  no-more')
    sleep(2)
    command('quit')
    value = decoder(comm)
    fail = failChecker(value)
    rePwr = check(value, conditionPwr)
    reTemp = check(value, conditionTemp)
    if fail == None and rePwr != None:
        (_, eT) = reTemp.span()
        (_, eP) = rePwr.span()
        PWR = value[eP: eP + 6]
        TEMP = value[eT: eT + 4].replace("\n", "").replace(" ", "")
        return (TEMP, PWR)
    else:
        if show:
            log(fail)
        return (TEMP, PWR)


