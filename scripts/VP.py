from datetime import datetime
from helpers.tableConverter import clientsTable
from helpers.formatter import colorFormatter


def verifyPort(comm, command):
    keep = True
    while keep == True:
        FRAME = input("Ingrese frame de clientes : ").upper()
        SLOT = input("Ingrese slot de clientes : ").upper()
        PORT = input("Ingrese puerto de los clientes : ").upper()
        lst = [{"fsp": f"{FRAME}/{SLOT}/{PORT}"}]
        clients = clientsTable(comm, command, lst)
        print(
            "| {:^5} | {:^5} | {:^5} | {:^5} | {:^35} | {:^10} | {:^15} | {:^10} | {:^10} |".format(
                "FRAME", "SLOT", "PORT", "ID", "NAME", "STATUS", "CAUSE", "TIME", "DATE"
            )
        )
        for client in clients:
            ID = client["id"]
            NAME = client["name"]
            STATUS = str(client["status"]).replace(" ", "").replace(" \n", "")
            CAUSE = str(client["cause"]).replace(" ", "").replace(" \n", "")
            TIME = client["ldt"]
            DATE = client["ldd"]
            resp = "| {:^5} | {:^5} | {:^5} | {:^5} | {:^35} | {:^10} | {:^15} | {:^10} | {:^10} |".format(
                FRAME, SLOT, PORT, ID, NAME, STATUS, CAUSE, TIME, DATE
            )
            CT = f"{DATE} {TIME}"
            if str(TIME) != "nan" and str(TIME) != "-":
                t1 = datetime.strptime(CT, "%Y-%m-%d %H:%M:%S")
                t2 = datetime.fromisoformat(str(datetime.now()))
                clientTime = t2 - t1
                color = "activated"
                if STATUS == "offline":
                    if CAUSE == "LOSi/LOBi" and clientTime.days <= 5:
                        color = "los1"
                    if CAUSE == "LOSi/LOBi" and clientTime.days > 5:
                        color = "los2"
                    elif CAUSE == "dying-gasp":
                        color = "off"
                    elif CAUSE == "deactive":
                        color = "suspended"
                    elif CAUSE == "nan":
                        color = "problems"
                    elif CAUSE != "LOSi/LOBi" and CAUSE != "dying-gasp" and CAUSE != "deactive" and CAUSE != "nan":
                        color = "unknown"
            resp = colorFormatter(resp, color)
            print(resp)

        preg = input("continuar? [Y | N] : ").upper()
        keep = True if preg == "Y" else False
