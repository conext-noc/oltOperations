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
newCondTime = "Ont autofind time   : "


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
        # (eFSP, _) = check(result, newCondFSPEnd).span()
        (_, eSN) = check(result, newCondSn).span()
        (_, eT) = check(result, newCondTime).span()
        aSN = result[eSN : eSN + 16].replace("\n", "").replace(" ", "")
        aFSP = result[sFSP : sFSP + 7].replace("\n", "").replace(" ", "")
        aT = result[eT : eT + 19].replace("\n", "")
        t1 = datetime.strptime(aT, "%Y-%m-%d %H:%M:%S")
        t2 = datetime.fromisoformat(str(datetime.now()))
        clientTime = t2 - t1
        client.append(
            {
                "fsp": aFSP.replace("\r", ""),
                "sn": aSN,
                "idx": ont + 1,
                "time": clientTime.days,
            }
        )
    log(f"| {'IDX':^3} | {'F/S/P':^6} | {'SN':^16} |", "normal")

    for ont in client:
        count = []
        if SN_NEW == ont["sn"] and ont["time"] <= 10:
            SN_FINAL = ont["sn"]
            FSP_FINAL = ont["fsp"]
            log(f"| {ont['idx']:^3} | {ont['fsp']:^6} | {ont['sn']:^16} |", "success")
            count.append({"sn": SN_FINAL, "fsp": FSP_FINAL})
        elif SN_NEW == ont["sn"] and ont["time"] > 10:
            log(f"| {ont['idx']:^3} | {ont['fsp']:^6} | {ont['sn']:^16} |", "warning")
        else:
            log(f"| {ont['idx']:^3} | {ont['fsp']:^6} | {ont['sn']:^16} |", "normal")
        if len(count) > 1:
            log(f"| {'IDX':^3} | {'F/S/P':^6} | {'SN':^16} |", "normal")
            res = {}
            for idx in count:
                res[idx] = {"sn": ont["sn"], "fsp": ont["fsp"]}
                log(
                    f"| {idx:^3} | {ont['fsp']:^6} | {ont['sn']:^16} |",
                    "normal",
                )
            ix = inp("SELECCIONE EL INDEX DEL SERIAL A UTILIZAR : ")
            SN_FINAL = res[ix]["sn"]
            FSP_FINAL = res[ix]["fsp"]
    return (SN_FINAL, FSP_FINAL)
