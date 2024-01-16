from time import sleep
from helpers.utils.decoder import decoder, check
from helpers.handlers.fail import fail_checker
from helpers.handlers.printer import log
from helpers.constants.regex_conditions import condition_onu_pwr, condition_onu_temp, condition_onu_pwr_rx
from helpers.utils.snmp import SNMP_get
from helpers.constants.snmp_data import *
from helpers.constants.definitions import *
from dotenv import load_dotenv
import os

load_dotenv()

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
        if re_pwr is not None and re_pwr_rx is not None:
            TEMP = re_temp.group(1)
            PWR = re_pwr.group(1)
            PWR_RX = re_pwr_rx.group(1)
    log(fail, "fail") if show and fail is not None else None
    return (TEMP, PWR, PWR_RX)

def optical_value_snmp(data):
    TEMP = None
    PWR = None
    PWR_RX = None
    for oid_port, fsp in map_ports.items():
        if fsp == data["fsp"]:
            TEMP = SNMP_get(os.getenv("SNMP_READ"),olt_devices[data["olt"]],SNMP_OIDS["TEMPERATURE"],161,oid_port,data["onu_id"])
            PWR_UNFORMAT = SNMP_get(os.getenv("SNMP_READ"),olt_devices[data["olt"]],SNMP_OIDS["POWER"],161,oid_port,data["onu_id"])
            PWR = (int(PWR_UNFORMAT)/100)
            PWR_RX_UNFORMAT = SNMP_get(os.getenv("SNMP_READ"),olt_devices[data["olt"]],SNMP_OIDS["POWER_RX_OLT"],161,oid_port,data["onu_id"])
            PWR_RX = ((int(PWR_RX_UNFORMAT) - 10000)/100)
    return (TEMP, PWR, PWR_RX)