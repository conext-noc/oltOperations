from time import sleep
from helpers.utils.decoder import decoder, check
from helpers.handlers.fail import fail_checker
from helpers.handlers.printer import log
from helpers.constants.regex_conditions import (
    condition_onu_last_down_cause,
    condition_onu_last_down_time,
    condition_onu_status,
)


def down_values(comm, command, data, show):
    command(f'  interface  gpon  {data["frame"]}/{data["slot"]}  ')
    command(f'  display  ont  info  {data["port"]}  {data["onu_id"]}  |  no-more')
    sleep(2)
    command("quit")
    value = decoder(comm)
    fail = fail_checker(value)
    re_cause_start = check(value, condition_onu_last_down_cause[0])
    re_cause_end = check(value, condition_onu_last_down_cause[1])
    re_time_start = check(value, condition_onu_last_down_time[0])
    re_time_end = check(value, condition_onu_last_down_time[1])
    re_status_start = check(value, condition_onu_status[0])
    re_status_end = check(value, condition_onu_status[1])

    CAUSE = None
    TIME = None
    DATE = None
    STATUS = None

    if fail is not None and re_cause_start is None:
        log(fail, "fail") if show else None
        return (CAUSE, TIME, DATE, STATUS)

    (_, s_c) = re_cause_start.span()
    (e_c, _) = re_cause_end.span()
    (_, s_t) = re_time_start.span()
    (e_t, _) = re_time_end.span()
    (_, s_s) = re_status_start.span()
    (e_s, _) = re_status_end.span()

    CAUSE = value[s_c : e_c - 2].replace("\n", "").replace("\r", "")
    STATUS = value[s_s : e_s - 2].replace("\n", "").replace("\r", "")
    TIME_DATE = value[s_t : e_t - 2].replace("\n", "").replace("\r", "")
    if TIME_DATE != "-":
        DATE = value[s_t : e_t - 2].replace("\n", "").replace("\r", "").split(" ")[0]
        TIME = value[s_t : e_t - 2].replace("\n", "").replace("\r", "").split(" ")[1]
    else:
        DATE = "-"
        TIME = "-"
    return (CAUSE, TIME, DATE, STATUS)
