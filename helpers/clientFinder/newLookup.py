from datetime import datetime
from time import sleep
from helpers.utils.decoder import check, checkIter, decoder
from helpers.utils.printer import colorFormatter, inp, log

condition = (
    "-----------------------------------------------------------------------------"
)
newCond = "----------------------------------------------------------------------------"
newCondFSP = "F/S/P               : "
newCondFSPEnd = "ONT NNI type"
newCondSn = "Ont SN              : "
newCondTime = "Ont autofind time   : "


def newLookup(comm, command, olt):
    SN_NEW = inp("Ingrese el Serial del Cliente a buscar : ").upper()
    SN_FINAL = None
    FSP_FINAL = None
    client = []
    command("display ont autofind all | no-more")
    sleep(5)
    value = decoder(comm)
    regex = checkIter(value, newCond)
    for ont in range(len(regex) - 1):
        (_, s) = regex[ont]
        (e, _) = regex[ont + 1]
        result = value[s:e]
        (_, sFSP) = check(result, newCondFSP).span()
        # (eFSP, _) = check(result, newCondFSPEnd).span()
        (_, eSN) = check(result, newCondSn).span()
        (_, eT) = check(result, newCondTime).span()
        aSN = result[eSN : eSN + 16].replace("\n", "").replace(" ", "")
        aFSP = result[sFSP : sFSP+7].replace("\n", "").replace(" ", "")
        aT = result[eT : eT + 19].replace("\n", "")
        t1 = datetime.strptime(aT, "%Y-%m-%d %H:%M:%S")
        t2 = datetime.fromisoformat(str(datetime.now()))
        clientTime = t2 - t1
        client.append({"fsp": aFSP.replace("\r",""), "sn": aSN, "idx": ont + 1, "time": clientTime.days})
    log("| {:^3} | {:^6} | {:^16} |".format("IDX", "F/S/P", "SN"))
    
    for ont in client:
        count = []
        if SN_NEW == ont["sn"] and ont["time"] <= 10:
            SN_FINAL = ont["sn"]
            FSP_FINAL = ont["fsp"]
            log(
                colorFormatter(
                    "| {:^3} | {:^6} | {:^16} |".format(ont["idx"],ont["fsp"],ont["sn"]), "success"
                )
            )
            count.append({"sn": SN_FINAL, "fsp": FSP_FINAL})
        elif SN_NEW == ont["sn"] and ont["time"] > 10:
            log(
                colorFormatter(
                    "| {:^3} | {:^6} | {:^16} |".format(ont["idx"],ont["fsp"],ont["sn"]), "warning"
                )
            )
        else:
            log("| {:^3} | {:^6} | {:^16} |".format(ont["idx"],ont["fsp"],ont["sn"]))
        if len(count) > 1:
            log("| {:^3} | {:^6} | {:^16} |".format("IDX", "F/S/P", "sn"))
            for idx, res in enumerate(count):
                log("| {:^3} | {:^6} | {:^16} |".format(idx, res["fsp"], res["sn"]))
            ix = inp("SELECCIONE EL INDEX DEL SERIAL A UTILIZAR : ")
            SN_FINAL = res[ix]["sn"]
            FSP_FINAL = res[ix]["fsp"]
    return (SN_FINAL, FSP_FINAL)
