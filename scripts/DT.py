from helpers.clientsData import clientsTable
from helpers.printer import log,colorFormatter
from datetime import datetime


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
portCountX15 = {"0/1/0": 0,
               "0/1/1": 0,
               "0/1/2": 0,
               "0/1/3": 0,
               "0/1/4": 0,
               "0/1/5": 0,
               "0/1/6": 0,
               "0/1/7": 0,
               "0/1/8": 0,
               "0/1/9": 0,
               "0/1/10": 0,
               "0/1/11": 0,
               "0/1/12": 0,
               "0/1/13": 0,
               "0/1/14": 0,
               "0/1/15": 0,
               "0/2/0": 0,
               "0/2/1": 0,
               "0/2/2": 0,
               "0/2/3": 0,
               "0/2/4": 0,
               "0/2/5": 0,
               "0/2/6": 0,
               "0/2/7": 0,
               "0/2/8": 0,
               "0/2/9": 0,
               "0/2/10": 0,
               "0/2/11": 0,
               "0/2/12": 0,
               "0/2/13": 0,
               "0/2/14": 0,
               "0/2/15": 0,
               "0/3/0": 0,
               "0/3/1": 0,
               "0/3/2": 0,
               "0/3/3": 0,
               "0/3/4": 0,
               "0/3/5": 0,
               "0/3/6": 0,
               "0/3/7": 0,
               "0/3/8": 0,
               "0/3/9": 0,
               "0/3/10": 0,
               "0/3/11": 0,
               "0/3/12": 0,
               "0/3/13": 0,
               "0/3/14": 0,
               "0/3/15": 0,
               }
portCountX2 = {"0/1/0": 0,
               "0/1/1": 0,
               "0/1/2": 0,
               "0/1/3": 0,
               "0/1/4": 0,
               "0/1/5": 0,
               "0/1/6": 0,
               "0/1/7": 0,
               "0/1/8": 0,
               "0/1/9": 0,
               "0/1/10": 0,
               "0/1/11": 0,
               "0/1/12": 0,
               "0/1/13": 0,
               "0/1/14": 0,
               "0/1/15": 0,
               "0/2/0": 0,
               "0/2/1": 0,
               "0/2/2": 0,
               "0/2/3": 0,
               "0/2/4": 0,
               "0/2/5": 0,
               "0/2/6": 0,
               "0/2/7": 0,
               "0/2/8": 0,
               "0/2/9": 0,
               "0/2/10": 0,
               "0/2/11": 0,
               "0/2/12": 0,
               "0/2/13": 0,
               "0/2/14": 0,
               "0/2/15": 0,
               }


def totalDeacts(comm, command, olt, quit):
    portToExec = ports[olt]
    portCount = portCountX15 if olt == "15" else portCountX2
    clients = clientsTable(comm, command, portToExec)
    log(
        "| {:^6} | {:^3} | {:^25} | {:^10} | {:^15} | {:^10} | {:^10} | {:^10} | {:^16} |".format(
            "F/S/P", "ID", "NAME", "STATUS", "CAUSE", "TIME", "DATE", "DEVICE", "SN"
        )
    )
    totalClients = len(clients)
    totalDeactM2M = 0
    totalDeactClients = 0
    for client in clients:
        FSP = str(client["fsp"])
        ID = client["id"]
        NAME = client["name"]
        STATUS = str(client["status"]).replace(" ", "").replace(" \n", "")
        SN = client["sn"]
        TP = client["ontType"]
        CAUSE = str(client["cause"]).replace(" ", "").replace(" \n", "")
        TIME = client["ldt"]
        DATE = client["ldd"]
        STATE = client["controlFlag"]
        resp = "| {:^6} | {:^3} | {:^25} | {:^10} | {:^15} | {:^10} | {:^10} | {:^10} | {:^16} |".format(
            FSP, ID, NAME, STATUS, CAUSE, TIME, DATE, TP, SN
        )
        CT = f"{DATE} {TIME}"
        if STATE == "deactivated":
            portCount[FSP] += 1
            totalDeactClients += 1
            if str(TIME) != "nan" and str(TIME) != "-":
                t1 = datetime.strptime(CT, "%Y-%m-%d %H:%M:%S")
                t2 = datetime.fromisoformat(str(datetime.now()))
                clientTime = t2 - t1
                color = ""
                if clientTime.days <= 60:
                    color = "suspended"
                if clientTime.days > 60:
                    color = "suspended+"
                    totalDeactM2M += 1
            resp = colorFormatter(resp, color)
            log(resp)
    for res in portCount.items():
        log("In Port {:^6} the total suspended are : {:^3}".format(res[0],res[1]))
    log(f"In olt {olt} the total suspended are {totalDeactClients}")
    log(f"In olt {olt} the total suspended with more than 2 Months are {totalDeactM2M}")
    log(f"In olt {olt} the total clients are {totalClients}")
