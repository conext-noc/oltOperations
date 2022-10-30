from datetime import datetime
from helpers.clientsTable import clientsTable
from helpers.formatter import colorFormatter


def verifyPort(comm, command):
    keep = True
    while keep == True:
        FRAME = input("Ingrese frame de clientes : ")
        SLOT = input("Ingrese slot de clientes : ")
        PORT = input("Ingrese puerto de los clientes : ")
        lst = [{"fsp": f"{FRAME}/{SLOT}/{PORT}"}]
        clients = clientsTable(comm,command,lst)
        print(
            "| {:^5} | {:^5} | {:^5} | {:^5} | {:^35} | {:^10} | {:^15} | {:^10} | {:^10} |".format(
                "FRAME", "SLOT", "PORT","ID", "NAME", "STATUS", "CAUSE", "TIME", "DATE"
            )
        )
        for client in clients:
            ID = client["id"]
            NAME = client["name"]
            STATUS = client["status"]
            CAUSE = client["cause"]
            TIME = client["ldt"]
            DATE = client["ldd"]
            resp = "| {:^5} | {:^5} | {:^5} | {:^5} | {:^35} | {:^10} | {:^15} | {:^10} | {:^10} |".format(
            FRAME,SLOT,PORT, ID, NAME, STATUS, CAUSE, TIME, DATE
            )
            CT = f"{DATE} {TIME}"
            if(str(TIME) != "nan"):
                t1 = datetime.strptime(CT, "%Y-%m-%d %H:%M:%S")
                t2 = datetime.fromisoformat(str(datetime.now()))
                clientTime = t2 - t1
                color = ""
                if (STATUS == "offline" and CAUSE == "LOSi/LOBi" and clientTime.days <= 5):
                    color = "los1" 
                if (STATUS == "offline" and CAUSE == "LOSi/LOBi" and clientTime.days > 5):
                    color = "los2" 
                elif (STATUS == "offline" and CAUSE == "dying-gasp"):
                    color = "off" 
                elif (STATUS == "offline" and CAUSE == "deactive"):
                    color = "suspended"
                else:
                    color = "activated"
                resp = colorFormatter(resp,color)
                print(resp)
            else:
                resp = colorFormatter(resp,"problems")
                print(resp)
        
        preg = input("continuar? [Y | N] : ")
        keep = True if preg == "Y" else False
