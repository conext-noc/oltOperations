from datetime import datetime
from time import sleep
from helpers.utils.decoder import check, check_iter, decoder
from helpers.handlers.printer import inp, log

condition = (
    "-----------------------------------------------------------------------------"
)
newCond = "----------------------------------------------------------------------------"
newCondFSP = "F/S/P               : "
newCondFSPEnd = "ONT NNI type"
newCondSn = "Ont SN              : "


def new_lookup(comm, command, SN_NEW):
    SN_FINAL = None
    FSP_FINAL = None
    client = []
    command("display ont autofind all | no-more")
    sleep(5)
    value = decoder(comm)
    regex = check_iter(value, newCond)
    for ont in range(len(regex) - 1):
        (_, s) = regex[ont]
        (e, _) = regex[ont + 1]
        result = value[s:e]
        (_, sFSP) = check(result, newCondFSP).span()
        (_, eSN) = check(result, newCondSn).span()
        aSN = result[eSN : eSN + 16].replace("\n", "").replace(" ", "")
        aFSP = result[sFSP : sFSP + 7].replace("\n", "").replace(" ", "")
        client.append(
            {
                "fsp": aFSP.replace("\r", ""),
                "sn": aSN,
                "idx": ont + 1
            }
        )
    log(f"| {'IDX':^3} | {'F/S/P':^6} | {'SN':^16} |", "normal")

    for ont in client:
        if SN_NEW == ont["sn"]:
            SN_FINAL = ont["sn"]
            FSP_FINAL = ont["fsp"]
    return (SN_FINAL, FSP_FINAL)
