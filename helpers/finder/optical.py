from time import sleep
from helpers.utils.decoder import decoder, check
from helpers.handlers.fail import fail_checker
from helpers.handlers.printer import log
from helpers.constants.regex_conditions import condition_onu_pwr, condition_onu_temp, condition_onu_pwr_rx

OPTICAL_TIME = 8
PWR_LEN = 6
TEMP_LEN = 4

def optical_values(comm, command, data, show):
    TEMP = None
    PWR = None
    PWR_RX = None
    sleep(OPTICAL_TIME)
    command(f'  interface  gpon  {data["frame"]}/{data["slot"]}  ')
    sleep(OPTICAL_TIME)
    command(
        f'  display  ont  optical-info  {data["port"]}  {data["onu_id"]}  |  no-more'
    )
    sleep(OPTICAL_TIME)
    command("quit")
    value = decoder(comm)
    fail = fail_checker(value)
    re_pwr = check(value, condition_onu_pwr)
    re_pwr_rx = check(value, condition_onu_pwr_rx)
    re_temp = check(value, condition_onu_temp)
    if fail is None:
        if re_pwr is not None:
            (_, eT) = re_temp.span()
            (_, eP) = re_pwr.span()
            (_, ePRx) = re_pwr_rx.span()
            
            PWR = value[eP : eP + PWR_LEN]
            TEMP = (
                value[eT : eT + TEMP_LEN].replace("\n", "").replace(" ", "").replace("\r", "")
            )
            PWR_RX = value[ePRx : ePRx + PWR_LEN]
    log(fail, "fail") if show and fail is not None else None
    return (TEMP, PWR, PWR_RX)
