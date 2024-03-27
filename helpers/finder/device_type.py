import re
from time import sleep
from helpers.utils.decoder import check_iter, decoder
from helpers.handlers.fail import fail_checker

def type_finder(comm, command, data):
    ONT_VENDOR = None
    ONT_EQUIPMENT_ID = None
    ONT_VERSION = None
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
        ONT_EQUIPMENT_ID = (
            re.sub(
                " +",
                " ",
                re.search(r"Equipment-ID\s+:\s+[^\n]+", output[start:end]).group(),
            )
            .replace(" \r", "")
            .replace("Equipment-ID : ", "")
        )
        [(_, start), (end, _)] = regex
        ONT_VERSION = (
            re.sub(
                " +",
                " ",
                re.search(r"Main Software Version :\s+:\s+[^\n]+", output[start:end]).group(),
            )
            .replace(" \r", "")
            .replace("Main Software Version : : ", "")
        )
        print(ONT_VERSION)
    command("quit")
    ONT_VENDOR = "HWTC" if "1126" != ONT_EQUIPMENT_ID else "BDCM"
    return (ONT_EQUIPMENT_ID, ONT_VENDOR, ONT_VERSION)
