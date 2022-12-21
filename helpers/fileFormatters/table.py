import re
from helpers.utils.decoder import checkIter, decoder
from time import sleep
from helpers.failHandler.fail import failChecker
from helpers.utils.printer import colorFormatter,log
from helpers.fileFormatters.fileHandler import dataToDict
from helpers.info.regexConditions import table


def clientsTable(comm, command, lst):
    CLIENTS = []
    for idx, lt in enumerate(lst):
        clientsSummary = []
        clientsPort = []
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
            valueStatePort = []
            valueNamesPort = []
            valueNamesSumm = []
            valueStateSumm = []
            reSumm = checkIter(value, table["conditionSummary"])
            rePort = checkIter(value, table["conditionPort"])
            for op in table["optionsSummary"]:
                name = op["name"]
                start = op["start"]
                end = op["end"]
                header = op["header"]
                (_, s) = reSumm[start]
                (e, _) = reSumm[end]
                if name == "names":
                    valueNamesSumm = dataToDict(header, value[s:e])
                else:
                    valueStateSumm = dataToDict(header, value[s:e])
            for op in table["optionsPort"]:
                name = op["name"]
                start = op["start"]
                end = op["end"]
                header = op["header"]
                (_, s) = rePort[start]
                (e, _) = rePort[end]
                if name == "names":
                    valueNamesPort = dataToDict(header, value[s:e])
                else:
                    valueStatePort = dataToDict(header, value[s:e])

            for (status, names) in zip(valueStateSumm, valueNamesSumm):
                if int(status["ID"]) == int(names["ID"]):
                    name = ""
                    for i in range(1, 11):
                        NAME = (
                            str(names[f"NAME{i}"])
                            if str(names[f"NAME{i}"]) != "nan"
                            else ""
                        )
                        name += NAME + " "
                    clientsSummary.append(
                        {
                            "fsp": fsp,
                            "frame": FRAME,
                            "slot": SLOT,
                            "port": PORT,
                            "id": status["ID"],
                            "name": re.sub(" +", " ", name).replace("\n", ""),
                            "status": status["State"],
                            "ldt": status["DownTime"],
                            "pwr": names["Rx/Tx power"].split("/")[0],
                            "ldd": status["DownDate"],
                            "cause": status["DownCause1"],
                            "sn": names["SN"],
                            "device": names["Type"],
                        }
                    )
            for (status, names) in zip(valueStatePort, valueNamesPort):
                if int(status["ID"]) == int(names["ID"]):
                    name = ""
                    for i in range(1, 11):
                        NAME = (
                            str(names[f"NAME{i}"])
                            if str(names[f"NAME{i}"]) != "nan"
                            else ""
                        )
                        name += NAME + " "
                    clientsPort.append(
                        {
                            "id": status["ID"],
                            "controlFlag": status["controlFlag"],
                            "name": name
                        }
                    )
            for (summ, port) in zip(clientsSummary, clientsPort):
                if summ["id"] == port["id"]:
                    CLIENTS.append(
                        {
                            "fsp": summ["fsp"],
                            "frame": FRAME,
                            "slot": SLOT,
                            "port": PORT,
                            "id": summ["id"],
                            "name": port["name"],
                            "status": summ["status"],
                            "pwr": summ["pwr"],
                            "controlFlag": port["controlFlag"],
                            "cause": summ["cause"],
                            "ldt": summ["ldt"],
                            "ldd": summ["ldd"],
                            "sn": summ["sn"],
                            "device": summ["device"],
                        }
                    )
            log(f"{idx} {fsp} done")
        else:
            resp = colorFormatter(fail, "fail")
            log(resp)
    return CLIENTS
