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
            reSumm = checkIter(value, table["condition_summary"])
            rePort = checkIter(value, table["condition_port"])
            for op in table["options_summary"]:
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
            for op in table["options_port"]:
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
                if int(status["onu_id"]) == int(names["onu_id"]):
                    name = ""
                    for i in range(1, 11):
                        NAME = (
                            str(names[f"name{i}"])
                            if str(names[f"name{i}"]) != "nan"
                            else ""
                        )
                        name += NAME + " "
                    clientsSummary.append(
                        {
                            "fsp": fsp,
                            "frame": FRAME,
                            "slot": SLOT,
                            "port": PORT,
                            "onu_id": status["onu_id"],
                            "name": re.sub(" +", " ", name).replace("\n", ""),
                            "status": status["state"],
                            "last_down_time": status["down_time"],
                            "pwr": names["rx_tx_power"].split("/")[0],
                            "last_down_date": status["down_date"],
                            "last_down_cause": status["down_cause_1"],
                            "sn": names["sn"],
                            "device": names["device"],
                        }
                    )
            for (status, names) in zip(valueStatePort, valueNamesPort):
                if int(status["onu_id"]) == int(names["onu_id"]):
                    name = ""
                    for i in range(1, 11):
                        NAME = (
                            str(names[f"name{i}"])
                            if str(names[f"name{i}"]) != "nan"
                            else ""
                        )
                        name += NAME + " "
                    clientsPort.append(
                        {
                            "onu_id": status["onu_id"],
                            "state": status["control_flag"],
                            "name": name
                        }
                    )
            for (summ, port) in zip(clientsSummary, clientsPort):
                if summ["onu_id"] == port["onu_id"]:
                    CLIENTS.append(
                        {
                            "fsp": summ["fsp"],
                            "frame": FRAME,
                            "slot": SLOT,
                            "port": PORT,
                            "onu_id": summ["onu_id"],
                            "name": port["name"],
                            "status": summ["status"],
                            "pwr": summ["pwr"],
                            "state": port["state"],
                            "last_down_cause": summ["last_down_cause"],
                            "last_down_time": summ["last_down_time"],
                            "last_down_date": summ["last_down_date"],
                            "sn": summ["sn"],
                            "device": summ["device"],
                        }
                    )
            log(f"{idx} {fsp} done")
        else:
            resp = colorFormatter(fail, "fail")
            log(resp)
    return CLIENTS
