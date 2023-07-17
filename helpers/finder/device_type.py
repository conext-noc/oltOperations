from time import sleep
from helpers.utils.decoder import check, decoder
from helpers.handlers.fail import fail_checker
from helpers.constants.definitions import ont_type_start, ont_type_end


def type_finder(comm, command, data):
    ONT_TYPE = None
    FAIL = None
    command(f"  interface  gpon  {data['frame']}/{data['slot']}  ")
    sleep(7)
    command(f"  display  ont  version  {data['port']}  {data['onu_id']}  ")
    sleep(7)
    command("quit")
    value = decoder(comm)
    FAIL = fail_checker(value)
    if FAIL is None:
        (_, tS) = check(value, ont_type_start).span()
        (tE, _) = check(value, ont_type_end).span()
        ONT_TYPE = value[tS:tE]
    return ONT_TYPE
