from helpers.fileFormatters.table import clientsTable
from helpers.utils.printer import colorFormatter, inp, log
from helpers.info.regexConditions import ports, vp_count
from helpers.operations.portHandler import portHandler, dictToZero
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
    FSP = None
    if action == "VP":
        FRAME = inp("Ingrese frame de cliente  : ")
        SLOT = inp("Ingrese slot de cliente   : ")
        PORT = inp("Ingrese puerto de cliente : ")
        lst = [{"fsp": f"{FRAME}/{SLOT}/{PORT}"}]
    if action == "CA" or "DT" or "VT":
        lst = ports["olt"][olt]
        portCount = ports["count"][olt]
    while keep:
        clients = clientsTable(comm, command, lst, olt)
        totalClients = len(clients)
        totalDeactM2M = 0
        totalDeactClients = 0
        log(
            "| {:^6} | {:^6} | {:^40} | {:^11} | {:^7} | {:^15} | {:^6} | {:^14} | {:^14} | {:^10} | {:^16} | {:^10} | {:^8} |".format(
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
                "plan",
                "provider"
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
            PLAN = client["plan"]
            PROVIDER = client["vlan"]
            resp = "| {:^6} | {:^6} | {:^40} | {:^11} | {:^7} | {:^15} | {:^6} | {:^14} | {:^14} | {:^10} | {:^16} | {:^10} | {:^8} |".format(
                FSP, ID, NAME, STATE, STATUS, CAUSE,PWR, TIME, DATE, TP, SN, PLAN, PROVIDER
            )
            
            if action == "VP" or "VT":
                #Count for plans, providers and total clients
                portHandler(client)

                if CF == "active":
                    vp_count['1']['vp_active_cnt'] += 1
                    if STATUS == "offline":
                        if CAUSE == "LOSi/LOBi" or CAUSE == "LOS":
                            vp_count['1']['vp_los_cnt'] += 1
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
                            vp_count['1']['vp_off_cnt'] += 1
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
                    vp_count['1']['vp_deactive_cnt'] += 1
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
                        if clientTime.days <= 90:
                            color = "suspended"
                        if clientTime.days > 90:
                            color = "suspended+"
                            totalDeactM2M += 1
                    resp = colorFormatter(resp, color)
                    log(resp)
        log(f"""
En el puerto {FSP}:
El total de clientes en el puerto es           :   {vp_count['2']['vp_ttl']}
El total de clientes activos es                :   {vp_count['1']['vp_active_cnt']}
El total de clientes desactivados es           :   {vp_count['1']['vp_deactive_cnt']}
El total de clientes activos en corte es       :   {vp_count['1']['vp_los_cnt']}
El total de clientes activos apagados es       :   {vp_count['1']['vp_off_cnt']}

Proveedores :
El total de clientes con VNET es           :   {vp_count['2']['vp_vnet']}
El total de clientes con INTER es          :   {vp_count['2']['vp_inter']}
El total de clientes con IP PÚBLICA es     :   {vp_count['2']['vp_public_ip']}

Planes :
El total de clientes con Plan FAMILY        :   {vp_count['2']['OZ_0']}
El total de clientes con Plan MAX           :   {vp_count['2']['OZ_MAX']}
El total de clientes con Plan SKY           :   {vp_count['2']['OZ_SKY']}
El total de clientes con Plan MAGICAL       :   {vp_count['2']['OZ_MAGICAL']}
El total de clientes con Plan NEXT          :   {vp_count['2']['OZ_NEXT']}
El total de clientes con Plan PLUS          :   {vp_count['2']['OZ_PLUS']}
El total de clientes con Planes DEDICADOS   :   {vp_count['2']['OZ_DEDICADO']}
El total de clientes con Plan CONECTA       :   {vp_count['2']['OZ_CONECTA']}
El total de Clientes sin Plan Asignado      :   {vp_count['2']['NA']}
""")if action == "VP" or "VT" else None
        dictToZero(vp_count['1'])
        dictToZero(vp_count['2'])
        preg = inp("continuar? [Y | N] : ") if action == "VP" else None
        FRAME = inp("Ingrese frame de cliente  : ") if action == "VP" and preg == "Y" else None
        SLOT = inp("Ingrese slot de cliente   : ") if action == "VP" and preg == "Y" else None
        PORT = inp("Ingrese puerto de cliente : ") if action == "VP" and preg == "Y" else None
        lst = [{"fsp": f"{FRAME}/{SLOT}/{PORT}"}] if action == "VP" and preg == "Y" else None
        keep = True if preg == "Y" else False
        if action == "DT":
            for res in portCount.items():
                log("In Port {:^6} the total suspended are : {:^3}".format(res[0],res[1]))
            log(f"In olt {olt} the total suspended are {totalDeactClients}")
            log(f"In olt {olt} the total suspended with more than 3 Months are {totalDeactM2M}")
            log(f"In olt {olt} the total clients are {totalClients}")
