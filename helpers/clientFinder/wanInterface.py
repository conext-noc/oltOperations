from helpers.utils.decoder import decoder, check
from helpers.failHandler.fail import failChecker
from helpers.utils.printer import log


def preWan(comm, command, data):
    command(f"interface gpon {data['frame']}/{data['slot']}")
    command(f"display ont wan-info {data['port']} {data['id']}")
    command("quit")
    value = decoder(comm)
    re = check(value, "Manage VLAN                : ")
    fail = failChecker(value)
    if fail == None:
        (_, e) = re.span()
        vUsed = value[e: e + 4]
        log(f"Al ONT se le ha agregado la vlan {vUsed}")
        return vUsed
    else:
        log(fail)
        return fail