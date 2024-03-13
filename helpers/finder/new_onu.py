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
    value = decoder(comm)
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
        fsp_data_regex = check(result, newCondFSP)
        if fsp_data_regex is None:
            continue
        (_, sFSP) = fsp_data_regex.span()
        # (eFSP, _) = check(result, newCondFSPEnd).span()
        sn_data_regex = check(result, newCondSn)
        if sn_data_regex is None:
            continue
        (_, eSN) = sn_data_regex.span()
        aSN = result[eSN : eSN + 16].replace("\n", "").replace(" ", "")
        aFSP = result[sFSP : sFSP + 7].replace("\n", "").replace(" ", "")
        client.append({"fsp": aFSP.replace("\r", ""), "sn": aSN, "idx": ont + 1})
    log("| {:^3} | {:^6} | {:^16} |".format("IDX", "F/S/P", "SN"), "normal")

    for ont in client:
        count = []
        if SN_NEW == ont["sn"]:
            SN_FINAL = ont["sn"]
            FSP_FINAL = ont["fsp"]
            log(
                "| {:^3} | {:^6} | {:^16} |".format(ont["idx"], ont["fsp"], ont["sn"]),
                "success",
            )
            count.append({"sn": SN_FINAL, "fsp": FSP_FINAL})
        else:
            log("| {:^3} | {:^6} | {:^16} |".format(ont["idx"], ont["fsp"], ont["sn"]), "normal")
        if len(count) > 1:
            log("| {:^3} | {:^6} | {:^16} |".format("IDX", "F/S/P", "sn"), "normal")
            for idx, res in enumerate(count):
                log("| {:^3} | {:^6} | {:^16} |".format(idx, res["fsp"], res["sn"]))
            ix = inp("SELECCIONE EL INDEX DEL SERIAL A UTILIZAR : ")
            SN_FINAL = res[ix]["sn"]
            FSP_FINAL = res[ix]["fsp"]
    return (SN_FINAL, FSP_FINAL)
