from datetime import datetime
from helpers.formatter import colorFormatter
from helpers.clientsData import clientsTable


def verifyPort(comm, command):
    keep = True
    while keep == True:
        FRAME = input("Ingrese frame de clientes : ").upper()
        SLOT = input("Ingrese slot de clientes : ").upper()
        PORT = input("Ingrese puerto de los clientes : ").upper()
        lst = [{"fsp": f"{FRAME}/{SLOT}/{PORT}"}]
        clients = clientsTable(comm, command, lst)
        print(
        "| {:^6} | {:^3} | {:^35} | {:^10} | {:^15} | {:^10} | {:^10} | {:^10} | {:^16} |".format(
            "F/S/P", "ID", "NAME", "STATUS", "CAUSE", "TIME", "DATE", "DEVICE", "SN"
        )
    )
        for client in clients:
            FSP = client["fsp"]
            ID = client["id"]
            NAME = client["name"]
            STATUS = str(client["status"]).replace(" ", "").replace(" \n", "")
            CF = client["controlFlag"]
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
                t1 = datetime.strptime(CT, "%Y-%m-%d %H:%M:%S")
                t2 = datetime.fromisoformat(str(datetime.now()))
                clientTime = t2 - t1
                color = "activated"
                if CF == "active":
                    if STATUS == "offline" and (CAUSE == "LOSi/LOBi" or CAUSE == "LOS") and clientTime.days <= 5:
                        color = "los1"
                    if STATUS == "offline" and (CAUSE == "LOSi/LOBi" or CAUSE == "LOS") and clientTime.days > 5:
                        color = "los2"
                    elif STATUS == "offline" and CAUSE == "dying-gasp" and clientTime.days <= 10:
                        color = "off"
                    elif STATUS == "offline" and CAUSE == "dying-gasp" and clientTime.days > 10:
                        color = "suspended"
                    elif STATUS == "offline" and CAUSE == "nan":
                        color = "problems"
                    elif STATUS == "offline" and CAUSE != "LOSi/LOBi" and CAUSE != "dying-gasp" and CAUSE != "deactive" and CAUSE != "nan":
                        color = "unknown"
                    else:
                        color = "activated"
                else:
                    color = "suspended"
            resp = colorFormatter(resp, color)
            print(resp)

        preg = input("continuar? [Y | N] : ").upper()
        keep = True if preg == "Y" else False
