from helpers.clientsData import clientsTable
from helpers.printer import log,colorFormatter
from datetime import datetime
from helpers.ports import ports

def clientFault(comm, command, olt):
    portToExec = ports[olt]
    clients = clientsTable(comm, command, portToExec)
    log(
        "| {:^6} | {:^3} | {:^35} | {:^10} | {:^15} | {:^10} | {:^10} | {:^10} | {:^16} |".format(
            "F/S/P", "ID", "NAME", "STATUS", "CAUSE", "TIME", "DATE", "DEVICE", "SN"
        )
    )
    for client in clients:
        FSP = client["fsp"]
        ID = client["id"]
        NAME = client["name"]
        STATUS = str(client["status"]).replace(" ", "").replace(" \n", "")
        SN = client["sn"]
        TP = client["ontType"]
        CAUSE = str(client["cause"]).replace(" ", "").replace(" \n", "")
        TIME = client["ldt"]
        DATE = client["ldd"]
        resp = "| {:^6} | {:^3} | {:^35} | {:^10} | {:^15} | {:^10} | {:^10} | {:^10} |{:^16} |".format(
            FSP, ID, NAME, STATUS, CAUSE, TIME, DATE, TP,SN
        )
        CT = f"{DATE} {TIME}"
        if str(TIME) != "nan" and str(TIME) != "-":
            if STATUS == "offline":
                if CAUSE == "LOSi/LOBi" or CAUSE == "LOS":
                    t1 = datetime.strptime(CT, "%Y-%m-%d %H:%M:%S")
                    t2 = datetime.fromisoformat(str(datetime.now()))
                    clientTime = t2 - t1
                    color = ""
                    if clientTime.days <= 5:
                        color = "los1"
                    if clientTime.days > 5:
                        color = "los2"
                    resp = colorFormatter(resp, color)
                    log(resp)
