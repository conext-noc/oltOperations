from helpers.fileFormatters.table import clientsTable
from helpers.utils.printer import colorFormatter, inp, log
from helpers.info.regexConditions import ports
from datetime import datetime


def portOperation(comm, command, quit, olt, action):
    """
    comm        :   ssh connection handler [class]
    command     :   sends ssh commands [func]
    quit        :   terminates the ssh connection [func]
    olt         :   defines the selected olt [var:str]
    action      :   defines the type of lookup/action of the client [var:str]
    
    This module requests the status of a given port on the olt
    """
    keep = True
    lst = []
    portCount = []
    vp_active_cnt = 0
    vp_deactive_cnt = 0
    vp_los_cnt = 0
    vp_off_cnt = 0
    vp_ttl = 0
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
            "| {:^6} | {:^6} | {:^40} | {:^11} | {:^7} | {:^15} | {:^6} | {:^24} | {:^24} | {:^10} | {:^16} |".format(
                "f/s/p",
                "onu_id",
                "name",
                "state",
                "status",
                "last_down_cause",
                "pwr",
                "last_down_time",
                "last_down_date",
                "device",
                "sn",
            )
        )
        for client in clients:
            FSP = client["fsp"]
            ID = client["onu_id"]
            NAME = client["name"][:40]
            STATUS = str(client["status"]).replace(" ", "").replace(" \n", "")
            STATE = client["state"]
            CF = client["state"]
            SN = client["sn"]
            TP = client["device"]
            CAUSE = str(client["last_down_cause"]).replace(" ", "").replace(" \n", "")
            TIME = client["last_down_time"]
            DATE = client["last_down_date"]
            PWR = client["pwr"]
            CT = f"{DATE} {TIME}"
            resp = "| {:^6} | {:^6} | {:^40} | {:^11} | {:^7} | {:^15} | {:^6} | {:^24} | {:^24} | {:^10} | {:^16} |".format(
                FSP, ID, NAME, STATE, STATUS, CAUSE,PWR, TIME, DATE, TP, SN
            )
            if action == "VP":
                vp_ttl += 1
                if CF == "active":
                    vp_active_cnt += 1
                    if STATUS == "offline":
                        if CAUSE == "LOSi/LOBi" or CAUSE == "LOS":
                            vp_los_cnt += 1
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
                            vp_off_cnt += 1
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
                    vp_deactive_cnt += 1
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
                    color = ""
                    totalDeactClients += 1
                    if str(TIME) != "nan" and str(TIME) != "-":
                        t1 = datetime.strptime(CT, "%Y-%m-%d %H:%M:%S")
                        t2 = datetime.fromisoformat(str(datetime.now()))
                        clientTime = t2 - t1
                        if clientTime.days <= 60:
                            color = "suspended"
                        if clientTime.days > 60:
                            color = "suspended+"
                            totalDeactM2M += 1
                    resp = colorFormatter(resp, color)
                    log(resp)
        log(f"""
En el puerto {FSP}:
El total del clientes en el puerto es       :   {vp_ttl}
El total del clientes activos es            :   {vp_active_cnt}
El total del clientes desactivados es       :   {vp_deactive_cnt}
El total del clientes activos en corte es   :   {vp_los_cnt}
El total del clientes activos apagados es   :   {vp_off_cnt}

                    """) if action == "VP" else None
        preg = inp("continuar? [Y | N] : ") if action == "VP" else None
        vp_active_cnt = 0
        vp_deactive_cnt = 0
        vp_los_cnt = 0
        vp_off_cnt = 0
        vp_ttl = 0
        FRAME = inp("Ingrese frame de cliente  : ") if action == "VP" and preg == "Y" else None
        SLOT = inp("Ingrese slot de cliente   : ") if action == "VP" and preg == "Y" else None
        PORT = inp("Ingrese puerto de cliente : ") if action == "VP" and preg == "Y" else None
        lst = [{"fsp": f"{FRAME}/{SLOT}/{PORT}"}] if action == "VP" and preg == "Y" else None
        keep = True if preg == "Y" else False
        if action == "DT":
            for res in portCount.items():
                log("In Port {:^6} the total suspended are : {:^3}".format(res[0],res[1]))
            log(f"In olt {olt} the total suspended are {totalDeactClients}")
            log(f"In olt {olt} the total suspended with more than 2 Months are {totalDeactM2M}")
            log(f"In olt {olt} the total clients are {totalClients}")
