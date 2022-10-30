from helpers.outputDecoder import parser, txt2csvFormatter
from helpers.csvParser import parserCSV
import re
from time import sleep
import os

condition = (
    "------------------------------------------------------------------------------"
)

options = [
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


def clientsTable(comm, command, lst):
    CLIENTS = []
    for idx, lt in enumerate(lst):
        fsp = lt["fsp"]
        command(f"display ont info summary {fsp} | no-more")
        sleep(3)
        (valueRES, regex) = parser(comm, condition, "m")
        for op in options:
            name = op["name"]
            start = op["start"]
            end = op["end"]
            header = op["header"]
            (_, s) = regex[start]
            (e, _) = regex[end]
            val = re.sub(" +", " ", valueRES[s:e]).replace(" ", ",")
            print(val, file=open(f"{name}{idx}.txt", "w"))
            txt2csvFormatter(f"{name}{idx}.txt")
            value = open(f"{name}{idx}.txt", "r").read().replace(" +", "")
            os.remove(f"{name}{idx}.txt")
            print(header + value, file=open(f"{name}{idx}.txt", "w"))
            data = open(f"{name}{idx}.txt", "r").read().replace(" +", "")
            os.remove(f"{name}{idx}.txt")
            print(data, file=open(f"{name}{idx}.csv", "w"))
        valueState = parserCSV(f"state{idx}.csv")
        valueNames = parserCSV(f"names{idx}.csv")
        for (status, names) in zip(valueState, valueNames):
            if status["ID"] == names["ID"] :
                ID = status["ID"]
                STATUS = status["State"]
                TIME = status["DownTime"]
                DATE = status["DownDate"]
                SN = names["SN"]
                ONT_TYPE = names["Type"]
                name = ""
                CAUSE = status["DownCause1"]
                for i in range(1, 11):
                    NAME = (
                        str(names[f"NAME{i}"])
                        if str(names[f"NAME{i}"]) != "nan"
                        else ""
                    )
                    name += NAME + " "
                CLIENTS.append({"fsp":fsp,"id": ID,"name":name.replace(" +", "").replace("\n", ""), "status":STATUS, "ldt":TIME, "ldd": DATE, "cause":CAUSE, "sn": SN, "ontType": ONT_TYPE})
        os.remove(f"state{idx}.csv")
        os.remove(f"names{idx}.csv")
    return CLIENTS
