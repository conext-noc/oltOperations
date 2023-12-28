import re
from helpers.utils.decoder import check_iter, decoder
from helpers.handlers.fail import fail_checker

def type_finder(comm, command, data):
    ONT_VENDOR = None
    ONT_EQUIPMENT_ID = None
    FAIL = None
    command(f"interface gpon {data['frame']}/{data['slot']}")
    command(f"display ont version {data['port']} {data['onu_id']}")
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
    command("quit")
    ONT_VENDOR = "HWTC" if "1126" != ONT_EQUIPMENT_ID else "BDCM"
    return (ONT_EQUIPMENT_ID, ONT_VENDOR)
