from helpers.fileFormatters.table import clientsTable
from helpers.utils.printer import colorFormatter, inp, log
from helpers.info.regexConditions import ports
from datetime import datetime


def portOperation(comm, command, quit, olt, action):
    keep = True
    lst = []
    portCount = []
    if action == "VP":
        FRAME = inp("Ingrese frame de cliente  : ")
        SLOT = inp("Ingrese slot de cliente   : ")
        PORT = inp("Ingrese puerto de cliente : ")
        lst = [{"fsp": f"{FRAME}/{SLOT}/{PORT}"}]
    if action == "CA":
        lst = ports["olt"][olt]
        portCount = ports["count"][olt]
    if action == "DT":
        lst = ports["olt"][olt]
        portCount = ports["count"][olt]
    while keep:
        clients = clientsTable(comm, command, lst)
        totalClients = len(clients)
        totalDeactM2M = 0
        totalDeactClients = 0
        log(
            "| {:^6} | {:^3} | {:^56} | {:^11} | {:^10} | {:^15} | {:^6} | {:^10} | {:^10} | {:^10} | {:^16} |".format(
                "F/S/P",
                "ID",
                "NAME",
                "STATE",
                "STATUS",
                "CAUSE",
                "POWER",
                "TIME",
                "DATE",
                "DEVICE",
                "SN",
            )
        )
        for client in clients:
            FSP = client["fsp"]
            ID = client["id"]
            NAME = client["name"]
            STATUS = str(client["status"]).replace(" ", "").replace(" \n", "")
            STATE = client["controlFlag"]
            CF = client["controlFlag"]
            SN = client["sn"]
            TP = client["device"]
            CAUSE = str(client["cause"]).replace(" ", "").replace(" \n", "")
            TIME = client["ldt"]
            DATE = client["ldd"]
            PWR = client["pwr"]
            resp = "| {:^6} | {:^3} | {:^56} | {:^11} | {:^10} | {:^15} | {:^6} | {:^10} | {:^10} | {:^10} | {:^16} |".format(
                FSP, ID, NAME, STATE, STATUS, CAUSE,PWR, TIME, DATE, TP, SN
            )
            if action == "VP":
                if CF == "active":
                    if STATUS == "offline":
                        if CAUSE == "LOSi/LOBi" or CAUSE == "LOS":
                            CT = f"{DATE} {TIME}"
                            if str(TIME) != "nan" and str(TIME) != "-":
                                t1 = datetime.strptime(CT, "%Y-%m-%d %H:%M:%S")
                                t2 = datetime.fromisoformat(str(datetime.now()))
                                clientTime = t2 - t1
                                color = "los1" if clientTime.days <= 5 else "los2"
                            else:
                                color = "warning"
                        elif CAUSE == "dying-gasp":
                            color = "off"
                        elif CAUSE == "nan":
                            color = "problems"
                        elif (
                            CAUSE != "LOSi/LOBi"
                            and CAUSE != "dying-gasp"
                            and CAUSE != "deactive"
                            and CAUSE != "nan"
                        ):
                            color = "unknown"
                    else:
                        color = "activated"
                else:
                    color = "suspended"
                log(colorFormatter(resp, color))
            if action == "CA":
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
            if action == "DT":
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
        preg = inp("continuar? [Y | N] : ") if action == "VP" else None
        FRAME = inp("Ingrese frame de cliente  : ") if action == "VP" else None
        SLOT = inp("Ingrese slot de cliente   : ") if action == "VP" else None
        PORT = inp("Ingrese puerto de cliente : ") if action == "VP" else None
        lst = [{"fsp": f"{FRAME}/{SLOT}/{PORT}"}] if action == "VP" else None
        keep = True if preg == "Y" else False
        if action == "DT":
            for res in portCount.items():
                log("In Port {:^6} the total suspended are : {:^3}".format(res[0],res[1]))
            log(f"In olt {olt} the total suspended are {totalDeactClients}")
            log(f"In olt {olt} the total suspended with more than 2 Months are {totalDeactM2M}")
            log(f"In olt {olt} the total clients are {totalClients}")