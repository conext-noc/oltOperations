from time import sleep
from helpers.utils.decoder import decoder, check
from helpers.handlers.fail import fail_checker
from helpers.handlers.printer import log
from helpers.constants.regex_conditions import condition_onu_pwr, condition_onu_temp


def optical_values(comm, command, data, show):
    TEMP = None
    PWR = None
    sleep(8)
    command(f'  interface  gpon  {data["frame"]}/{data["slot"]}  ')
    sleep(8)
    command(
        f'  display  ont  optical-info  {data["port"]}  {data["onu_id"]}  |  no-more'
    )
    sleep(8)
    command("quit")
    value = decoder(comm)
    fail = fail_checker(value)
    re_pwr = check(value, condition_onu_pwr)
    re_temp = check(value, condition_onu_temp)
    if fail is None:
        if re_pwr is not None:
            (_, eT) = re_temp.span()
            (_, eP) = re_pwr.span()
            PWR = value[eP : eP + 6]
            TEMP = (
                value[eT : eT + 4].replace("\n", "").replace(" ", "").replace("\r", "")
            )
    log(fail, "fail") if show and fail is not None else None
    return (TEMP, PWR)
