from helpers.outputDecoder import checkIter, decoder
from helpers.fileHandler import fromCsv
import re
from time import sleep
import os
from helpers.failHandler import failChecker
from helpers.formatter import colorFormatter
from helpers.tableConverter import table2Dict

conditionSummary = "------------------------------------------------------------------------------"
conditionPort = "-----------------------------------------------------------------------------"

optionsSummary = [
    {
        "name": "state",
        "start": 2,
        "end": 3,
        "header": "ID,State,UpDate,UpTime,DownDate,DownTime,DownCause1,DownCause2,DownCause3,DownCause4,DownCause5,DownCause6,DownCause7,DownCause8\n",
    },
    {
        "name": "names",
        "start": 4,
        "end": 5,
        "header": "ID,SN,Type,Distance,Rx/Tx power,NAME1,NAME2,NAME3,NAME4,NAME5,NAME6,NAME7,NAME8,NAME9,NAME10\n",
    },
]
optionsPort = [
    {
        "name": "state",
        "start": 7,
        "end": 8,
        "header": "F/,S/P,ID,SN,controlFlag,runState,configState,matchState,protectSide,na\n",
    },
    {
        "name": "names",
        "start": 9,
        "end": 10,
        "header": "F/,S/P,ID,SN,NAME1,NAME2,NAME3,NAME4,NAME5,NAME6,NAME7,NAME8,NAME9,NAME10,NAME11,NAME12,NAME13,NAME14,NAME15,NAME16,NAME17,NAME18,NAME19,NAME20\n",
    },
]


def clientsTable(comm, command, lst):
    clientsSummary = []
    clientsPort = []
    CLIENTS = []
    for idx, lt in enumerate(lst):
        fsp = lt["fsp"]
        command(f"display ont info summary {fsp} | no-more")
        sleep(3)
        FRAME = int(fsp.split("/")[0])
        SLOT = int(fsp.split("/")[1])
        PORT = int(fsp.split("/")[2])
        command(f"display ont info {FRAME} {SLOT} {PORT} all  | no-more")
        sleep(3)
        value = decoder(comm)
        fail = failChecker(value)
        if fail == None:
            reSumm = checkIter(value, conditionSummary)
            rePort = checkIter(value, conditionPort)
            for op in optionsSummary:
                name = op["name"]
                start = op["start"]
                end = op["end"]
                header = op["header"]
                (_, s) = reSumm[start]
                (e, _) = reSumm[end]
                table2Dict(header, value[s:e], name, idx, "summ")
            for op in optionsPort:
                name = op["name"]
                start = op["start"]
                end = op["end"]
                header = op["header"]
                (_, s) = rePort[start]
                (e, _) = rePort[end]
                table2Dict(header, value[s:e], name, idx, "port")
            valueStateSumm = fromCsv(f"state{idx}summ.csv")
            valueNamesSumm = fromCsv(f"names{idx}summ.csv")
            valueStatePort = fromCsv(f"state{idx}port.csv")
            valueNamesPort = fromCsv(f"names{idx}port.csv")
            for (status, names) in zip(valueStateSumm, valueNamesSumm):
                if int(status["ID"]) == int(names["ID"]):
                    name = ""
                    for i in range(1, 11):
                        NAME = str(names[f"NAME{i}"]) if str(
                            names[f"NAME{i}"]) != "nan" else ""
                        name += NAME + " "
                    clientsSummary.append(
                        {
                            "fsp": fsp,
                            "id": status["ID"],
                            "name": re.sub(" +", " ", name).replace("\n", ""),
                            "status": status["State"],
                            "ldt": status["DownTime"],
                            "ldd": status["DownDate"],
                            "cause": status["DownCause1"],
                            "sn": names["SN"],
                            "ontType": names["Type"],
                        }
                    )
            for (status, names) in zip(valueStatePort, valueNamesPort):
                if int(status["ID"]) == int(names["ID"]):
                    clientsPort.append(
                        {
                            "id": status["ID"],
                            "controlFlag": status["controlFlag"],
                        }
                    )
            for (summ, port) in zip(clientsSummary, clientsPort):
                if (summ["id"] == port["id"]):
                    CLIENTS.append({
                        "fsp": summ["fsp"],
                        "id": summ["id"],
                        "name": summ["name"],
                        "status": summ["status"],
                        "controlFlag": port["controlFlag"],
                        "cause": summ["cause"],
                        "ldt": summ["ldt"],
                        "ldd": summ["ldd"],
                        "sn": summ["sn"],
                        "ontType": summ["ontType"],
                    })
            print(idx, fsp, "done")
            os.remove(f"state{idx}summ.csv")
            os.remove(f"names{idx}summ.csv")
            os.remove(f"state{idx}port.csv")
            os.remove(f"names{idx}port.csv")
        else:
            resp = colorFormatter(fail, "fail")
            print(resp)
    return CLIENTS
