from helpers.outputDecoder import parser, txt2csvFormatter
from helpers.csvParser import parser as csvParser
import re
from time import sleep
import os

condition = (
    "------------------------------------------------------------------------------"
)

ports = {
    "15": [
        {"fsp": "0/1/0"},
        {"fsp": "0/1/1"},
        {"fsp": "0/1/2"},
        {"fsp": "0/1/3"},
        {"fsp": "0/1/4"},
        {"fsp": "0/1/5"},
        {"fsp": "0/1/6"},
        {"fsp": "0/1/7"},
        {"fsp": "0/1/8"},
        {"fsp": "0/1/9"},
        {"fsp": "0/1/10"},
        {"fsp": "0/1/11"},
        {"fsp": "0/1/13"},
        {"fsp": "0/1/14"},
        {"fsp": "0/2/0"},
        {"fsp": "0/2/1"},
        {"fsp": "0/2/2"},
        {"fsp": "0/2/3"},
        {"fsp": "0/2/4"},
        {"fsp": "0/2/5"},
        {"fsp": "0/2/6"},
        {"fsp": "0/2/7"},
        {"fsp": "0/2/8"},
        {"fsp": "0/2/9"},
        {"fsp": "0/2/10"},
        {"fsp": "0/2/11"},
        {"fsp": "0/2/12"},
        {"fsp": "0/2/13"},
        {"fsp": "0/2/14"},
        {"fsp": "0/2/15"},
        {"fsp": "0/3/0"},
        {"fsp": "0/3/1"},
        {"fsp": "0/3/2"},
        {"fsp": "0/3/3"},
        {"fsp": "0/3/4"},
        {"fsp": "0/3/5"},
        {"fsp": "0/3/6"},
        {"fsp": "0/3/7"},
        {"fsp": "0/3/8"},
        {"fsp": "0/3/9"},
        {"fsp": "0/3/10"},
        {"fsp": "0/3/11"},
        {"fsp": "0/3/12"},
        {"fsp": "0/3/13"},
        {"fsp": "0/3/14"},
        {"fsp": "0/3/15"},
    ],
    "2": [
        {"fsp": "0/1/0"},
        {"fsp": "0/1/1"},
        {"fsp": "0/1/2"},
        {"fsp": "0/1/3"},
        {"fsp": "0/1/4"},
        {"fsp": "0/1/5"},
        {"fsp": "0/1/6"},
        {"fsp": "0/1/7"},
        {"fsp": "0/1/8"},
        {"fsp": "0/1/9"},
        {"fsp": "0/1/10"},
        {"fsp": "0/1/11"},
        {"fsp": "0/1/12"},
        {"fsp": "0/1/13"},
        {"fsp": "0/1/14"},
        {"fsp": "0/1/15"},
        {"fsp": "0/2/0"},
        {"fsp": "0/2/1"},
        {"fsp": "0/2/2"},
        {"fsp": "0/2/3"},
        {"fsp": "0/2/4"},
        {"fsp": "0/2/5"},
        {"fsp": "0/2/6"},
        {"fsp": "0/2/7"},
        {"fsp": "0/2/8"},
        {"fsp": "0/2/9"},
        {"fsp": "0/2/10"},
        {"fsp": "0/2/11"},
        {"fsp": "0/2/12"},
        {"fsp": "0/2/13"},
        {"fsp": "0/2/14"},
        {"fsp": "0/2/15"},
    ],
}

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


def clientFault(comm, command, olt):
    portToExec = ports[olt]
    print(
        "| {:^8} | {:^5} | {:^35} | {:^10} | {:^15} | {:^10} | {:^10} |".format(
            "F/S/P", "ID", "NAME", "STATUS", "CAUSE", "TIME", "DATE"
        )
    )
    for idx, selectedPorts in enumerate(portToExec):
        fsp = selectedPorts["fsp"]
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
        valueState = csvParser(f"state{idx}.csv")
        valueNames = csvParser(f"names{idx}.csv")
        for (status, names) in zip(valueState, valueNames):
            if (
                status["ID"] == names["ID"]
                and status["State"] == "offline"
                and status["DownCause1"] == "LOSi/LOBi"
            ):
                ID = status["ID"]
                STATUS = status["State"]
                TIME = status["DownTime"]
                DATE = status["DownDate"]
                name = ""
                CAUSE = status["DownCause1"]
                for i in range(1, 11):
                    NAME = (
                        str(names[f"NAME{i}"])
                        if str(names[f"NAME{i}"]) != "nan"
                        else ""
                    )
                    name += NAME + " "
                print(
                    "| {:^8} | {:^5} | {:^35} | {:^10} | {:^15} | {:^10} | {:^10} |".format(
                        fsp, ID, name, STATUS, CAUSE, TIME, DATE
                    )
                )
        os.remove(f"state{idx}.csv")
        os.remove(f"names{idx}.csv")
