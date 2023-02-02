from time import sleep
from helpers.failHandler.fail import failChecker
from helpers.fileFormatters.fileHandler import dataToDict
from helpers.utils.decoder import checkIter, decoder
from helpers.utils.printer import inp

infoHeader = "NA,F/,S/P,ID,SN,control_flag,run_state,config_state,match_state,protect_side,NA"
descHeader = "NA,F/,S/P,ID,NAME1,NAME2,NAME3,NAME4,NAME5,NAME6,NAME7,NA"

condition = "-----------------------------------------------------------------------------"
newCond = "----------------------------------------------------------------------------"
newCondFSP = "F/S/P               : "
newCondSn = "Ont SN              : "
newCondTime = "Ont autofind time   : "


def nameLookup(comm, command, quit):
    clients = []
    NAME = inp("Ingrese el Nombre del Cliente a buscar : ")
    command(f'display ont info by-desc "{NAME}" | no-more ')
    sleep(5)
    value = decoder(comm)
    regex = checkIter(value, condition)
    # print(value)
    FAIL = failChecker(value)
    portRange = []
    if FAIL == None:
        ttlPorts = len(regex) // 6
        for port in range(0, ttlPorts):
            portRange.append({"sInfo": regex[port+1][1], "eInfo": regex[port + 2]
                             [0], "sDesc": regex[port + 3][1], "eDesc": regex[port + 4][0]})
        for i in range(0,1):
            print("info",value[portRange[i]["sInfo"]:portRange[i]["eInfo"]])
            print("desc",value[portRange[i]["sDesc"]:portRange[i]["eDesc"]])
        for info in portRange:
            valueInfo = dataToDict(
                infoHeader, value[info["sInfo"]:info["eInfo"]])
            valueDesc = dataToDict(
                descHeader, value[info["sDesc"]:info["eDesc"]])
            for (info, desc) in zip(valueInfo, valueDesc):
                if info["ID"] == desc["ID"]:
                    name = ""
                    SLOT = int(desc["S/P"].split("/")[0])
                    PORT = int(desc["S/P"].split("/")[1])
                    for i in range(1, 7):
                        NAME = str(desc[f"NAME{i}"]) if str(
                            desc[f"NAME{i}"]) != "nan" else ""
                        name += NAME + " "
                    clients.append({
                        "frame": 0,
                        "slot": SLOT,
                        "port": PORT,
                        "id": desc["ID"],
                        "name": name,
                        "state": info["control_flag"],
                        "status": info["run_state"],
                        "sn": info["SN"]
                    })
        return {
            "data":clients,
            "fail": FAIL
        }
    quit()
    return {
            "data":clients,
            "fail": FAIL
        }
