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


def nameLookup(comm, command, NAME):
    clients = []
    command(f'display ont info by-desc "{NAME}" | no-more ')
    sleep(5)
    value = decoder(comm)
    regex = checkIter(value, condition)
    FAIL = failChecker(value)
    clients = []
    names = []
    statuses = []
    namesSTR = ""
    statuesSTR = ""
    if FAIL == None:
        ttlPorts = len(regex) // 6
        # Handling data
        for segment in range(0, ttlPorts):
            statuesSTR += value[regex[1 + 6*segment]
                                [1] + 1:regex[2 + 6 * segment][0] - 1]
            namesSTR += value[regex[3 + 6*segment]
                              [1] + 1:regex[4 + 6 * segment][0] - 1]

        # data conversion
        names = dataToDict(
            "NA,frame/,slot/port,onu_id,first_name,last_name,contract", namesSTR)
        statuses = dataToDict(
            "frame/,slot/port,onu_id,sn,state,status,match_state,config_state,x_state,NA", statuesSTR)
        for name in names.copy():
            if name.get("frame/") != "0/":
                names.remove(name)
        for status in statuses.copy():
            if status.get("frame/") != "0/":
                statuses.remove(status)

        # data parsing
        for (name, status) in zip(names, statuses):
            print(name)
            clients.append({
                "frame": "0",
                "slot": name["slot/port"].split("/")[0],
                "port": name["slot/port"].split("/")[1],
                "id": str(name["onu_id"])[:-2] if "." in str(name["onu_id"]) else str(name["onu_id"]),
                "name": f'{name["first_name"]} {name["last_name"]} {str(name["contract"]).zfill(10)}',
                "state": status["state"],
                "status": status["status"],
                "sn": status["sn"]
            })
        return {
            "data": clients,
            "fail": FAIL
        }