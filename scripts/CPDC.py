from helpers.clientsData import clientsTable
from helpers.getWanData import wan
from helpers.ports import ports


def cpdc(comm, command, OLT,quit):
    data = []
    FAIL = None
    portToExec = ports[OLT]
    clients = clientsTable(comm, command,portToExec)
    print(
        "| {:^10} | {:^35} | {:^16} | {:^10} | {:^10} | {:^10} | {:^6} | {:^6} | {:^6} | {:^10} | {:^6} | {:^6} | {:^6} | {:^10} | {:^6} | {:^6} | {:^6} | {:^10} |".format(
            "F/S/P/ID",
            "NAME",
            "SN",
            "TYPE",
            "STATUS",
            "STATE",
            "VLAN_1",
            "PLAN_1",
            "SPID_1",
            "STATE_1",
            "VLAN_2",
            "PLAN_2",
            "SPID_2",
            "STATE_2",
            "VLAN_3",
            "PLAN_3",
            "SPID_3",
            "STATE_3",
        )
    )
    for client in clients:
        FRAME = client["frame"]
        SLOT = client["slot"]
        PORT = client["port"]
        ID = client["id"]
        NAME = client["name"]
        SN = client["sn"]
        ONT_TYPE = client["ontType"]
        STATUS = str(client["status"]).replace(" ", "").replace(" \n", "")
        STATE = client["controlFlag"]
        (WAN, FAIL) = wan(comm, command, FRAME, SLOT, PORT, ID, OLT)
        if FAIL == None:
            if len(WAN) == 1:
                print(
                    "| {:^10} | {:^35} | {:^16} | {:^10} | {:^10} | {:^10} | {:^6} | {:^6} | {:^6} | {:^10} | {:^6} | {:^6} | {:^6} | {:^10} | {:^6} | {:^6} | {:^6} | {:^10} |".format(
                        f"{FRAME}/{SLOT}/{PORT}/{ID}",
                        NAME,
                        SN,
                        ONT_TYPE,
                        STATUS,
                        STATE,
                        WAN[0]["VLAN"],
                        WAN[0]["PLAN"],
                        WAN[0]["SPID"],
                        WAN[0]["STATE"],
                        "NA",
                        "NA",
                        "NA",
                        "NA",
                        "NA",
                        "NA",
                        "NA",
                        "NA",
                    )
                )
                data.append(
                    {
                        "frame": FRAME,
                        "slot": SLOT,
                        "port": PORT,
                        "id": ID,
                        "name": NAME,
                        "sn": SN,
                        "ont": ONT_TYPE,
                        "status": STATE,
                        "vlan_1": WAN[0]["VLAN"],
                        "plan_1": WAN[0]["PLAN"],
                        "spid_1": WAN[0]["SPID"],
                        "state_1": WAN[0]["STATE"],
                        "vlan_2": "NA",
                        "plan_2": "NA",
                        "spid_2": "NA",
                        "state_2": "NA",
                        "vlan_3": "NA",
                        "plan_3": "NA",
                        "spid_3": "NA",
                        "state_3": "NA",
                    }
                )
            if len(WAN) == 2:
                print(
                    "| {:^10} | {:^35} | {:^16} | {:^10} | {:^10} | {:^10} | {:^6} | {:^6} | {:^6} | {:^10} | {:^6} | {:^6} | {:^6} | {:^10} | {:^6} | {:^6} | {:^6} | {:^10} |".format(
                        f"{FRAME}/{SLOT}/{PORT}/{ID}",
                        NAME,
                        SN,
                        ONT_TYPE,
                        STATUS,
                        STATE,
                        WAN[0]["VLAN"],
                        WAN[0]["PLAN"],
                        WAN[0]["SPID"],
                        WAN[0]["STATE"],
                        WAN[1]["VLAN"],
                        WAN[1]["PLAN"],
                        WAN[1]["SPID"],
                        WAN[1]["STATE"],
                        "NA",
                        "NA",
                        "NA",
                        "NA",
                    )
                )
                data.append(
                    {
                        "frame": FRAME,
                        "slot": SLOT,
                        "port": PORT,
                        "id": ID,
                        "name": NAME,
                        "sn": SN,
                        "ont": ONT_TYPE,
                        "status": STATE,
                        "vlan_1": WAN[0]["VLAN"],
                        "plan_1": WAN[0]["PLAN"],
                        "spid_1": WAN[0]["SPID"],
                        "state_1": WAN[0]["SPID"],
                        "vlan_2": WAN[1]["VLAN"],
                        "plan_2": WAN[1]["PLAN"],
                        "spid_2": WAN[1]["SPID"],
                        "state_2": WAN[1]["SPID"],
                        "vlan_3": "NA",
                        "plan_3": "NA",
                        "spid_3": "NA",
                        "state_3": "NA",
                    }
                )
            if len(WAN) == 3:
                print(
                    "| {:^10} | {:^35} | {:^16} | {:^10} | {:^10} | {:^10} | {:^6} | {:^6} | {:^6} | {:^10} | {:^6} | {:^6} | {:^6} | {:^10} | {:^6} | {:^6} | {:^6} | {:^10} |".format(
                        f"{FRAME}/{SLOT}/{PORT}/{ID}",
                        NAME,
                        SN,
                        ONT_TYPE,
                        STATUS,
                        STATE,
                        WAN[0]["VLAN"],
                        WAN[0]["PLAN"],
                        WAN[0]["SPID"],
                        WAN[0]["STATE"],
                        WAN[1]["VLAN"],
                        WAN[1]["PLAN"],
                        WAN[1]["SPID"],
                        WAN[1]["STATE"],
                        WAN[2]["VLAN"],
                        WAN[2]["PLAN"],
                        WAN[2]["SPID"],
                        WAN[2]["STATE"],
                    )
                )
                data.append(
                    {
                        "frame": FRAME,
                        "slot": SLOT,
                        "port": PORT,
                        "id": ID,
                        "name": NAME,
                        "sn": SN,
                        "ont": ONT_TYPE,
                        "status": STATE,
                        "vlan_1": WAN[0]["VLAN"],
                        "plan_1": WAN[0]["PLAN"],
                        "spid_1": WAN[0]["SPID"],
                        "state_1": WAN[0]["STATE"],
                        "vlan_2": WAN[1]["VLAN"],
                        "plan_2": WAN[1]["PLAN"],
                        "spid_2": WAN[1]["SPID"],
                        "state_2": WAN[1]["STATE"],
                        "vlan_3": WAN[2]["VLAN"],
                        "plan_3": WAN[2]["PLAN"],
                        "spid_3": WAN[2]["SPID"],
                        "state_3": WAN[2]["STATE"],
                    }
                )
        else:
            print(
                "| {:^10} | {:^35} | {:^16} | {:^10} | {:^10} | {:^10} | {:^6} | {:^6} | {:^6} | {:^10} | {:^6} | {:^6} | {:^6} | {:^10} | {:^6} | {:^6} | {:^6} | {:^10} |".format(
                    f"{FRAME}/{SLOT}/{PORT}/{ID}",
                    NAME,
                    SN,
                    ONT_TYPE,
                    STATUS,
                    STATE,
                    "NA",
                    "NA",
                    "NA",
                    "NA",
                    "NA",
                    "NA",
                    "NA",
                    "NA",
                    "NA",
                    "NA",
                    "NA",
                    "NA",
                )
            )
            data.append(
                {
                    "frame": FRAME,
                    "slot": SLOT,
                    "port": PORT,
                    "id": ID,
                    "name": NAME,
                    "sn": SN,
                    "ont": ONT_TYPE,
                    "status": STATE,
                    "vlan_1": "NA",
                    "plan_1": "NA",
                    "spid_1": "NA",
                    "state_1": "NA",
                    "vlan_2": "NA",
                    "plan_2": "NA",
                    "state_2": "NA",
                    "spid_2": "NA",
                    "vlan_3": "NA",
                    "plan_3": "NA",
                    "spid_3": "NA",
                    "state_3": "NA",
                }
            )
    quit()
    return (data, FAIL)
