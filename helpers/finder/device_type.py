import re
from time import sleep
from helpers.utils.decoder import check_iter, decoder
from helpers.handlers.fail import fail_checker

def type_finder(comm, command, data):
    ONT_VENDOR = ""
    ONT_EQUIPMENT_ID = ""
    ONT_VERSION = ""
    FAIL = None
    command(f"interface gpon {data['frame']}/{data['slot']}")
    sleep(3)
    command(f"display ont version {data['port']} {data['onu_id']}")
    sleep(3)
    output = decoder(comm)
    FAIL = fail_checker(output)
    regex = check_iter(
        output,
        "--------------------------------------------------------------------------",
    )
    if len(regex) > 0 and FAIL is None:
        [(_, start), (end, _)] = regex
        id_match = re.search(r"Equipment-ID\s+:\s+([^\n]+)", output[start:end])
        if id_match:
            ONT_EQUIPMENT_ID = id_match.group(1).replace(" \r", "").replace("Equipment-ID : ", "")
        version_match = re.search(r"Main Software Version\s+:\s+(\S+)", output[start:end])
        if version_match:
            ONT_VERSION = version_match.group(1).replace(" \r", "").replace("Main Software Version    : ", "")
    command("quit")
    ONT_VENDOR = "HWTC" if "1126" != ONT_EQUIPMENT_ID else "BDCM"
    return (ONT_EQUIPMENT_ID, ONT_VENDOR, ONT_VERSION)
