from time import sleep
from helpers.utils.decoder import decoder, check
from helpers.handlers.fail import fail_checker
from helpers.handlers.printer import log
from helpers.constants.regex_conditions import (
    condition_onu_last_down_cause,
    condition_onu_last_down_time,
    condition_onu_status,
)
from helpers.utils.snmp import SNMP_get
import os
from dotenv import load_dotenv
from helpers.constants.definitions import olt_devices
from helpers.constants.snmp_data import SNMP_OIDS,map_ports, LAST_DOWN_CAUSE
load_dotenv()

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
    
    if re_cause_start is None:
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

def down_values_SNMP(data):
    CAUSE = None
    TIME = None
    DATE = None
    STATUS = None
    for oid_port, fsp in map_ports.items():
        if fsp == data["fsp"]:
            cause_unformat = SNMP_get(os.environ["SNMP_READ"],olt_devices[data["olt"]],SNMP_OIDS['LAST_DOWN_CAUSE'],161,oid_port,data["onu_id"])
            if cause_unformat in LAST_DOWN_CAUSE.keys():
                CAUSE = LAST_DOWN_CAUSE[cause_unformat]
                
            time_and_date_unformat = SNMP_get(os.environ["SNMP_READ"],olt_devices[data["olt"]],SNMP_OIDS['LAST_DOWN_TIME'],161,oid_port,data["onu_id"])
            YEAR = time_and_date_unformat[:6]
            MONTH = time_and_date_unformat[6:8]
            DAY = time_and_date_unformat[8:10]
            HOURS = time_and_date_unformat[10:12]
            MINUTE = time_and_date_unformat[12:14]
            SECONDS = time_and_date_unformat[14:16]
  
            DATE = f"{int(YEAR,16)}-{int(MONTH,16)}-{int(DAY,16)}"
            TIME = f"{int(HOURS,16)}:{int(MINUTE,16)}:{int(SECONDS,16)}"
            STATUS = SNMP_get(os.environ["SNMP_READ"],olt_devices[data["olt"]],SNMP_OIDS['STATUS'],161,oid_port,data["onu_id"])
    return (CAUSE, TIME, DATE, STATUS)
