import re

ontTypes = {
    "bridge_x15": (2, 2),
    "bridge_x2": (5, 6),
    "router_x15": (2, 2),
    "router_x2": (5, 3)
}

conditionONT = """ONTID :"""


def addONU(comm, sn, slot, port, provider, name, deviceType, commandToSend, enter):
    commandToSend(f"interface gpon 0/{slot}")
    enter()
    command = f"ont add {port} sn-auth {sn} omci ont-lineprofile-id {ontTypes[deviceType][0]} ont-srvprofile-id {ontTypes[deviceType][1]}  desc \"{name}\" "
    commandToSend(command)
    enter()
    enter()
    output = comm.recv(65535)
    output = output.decode("ascii")
    print(output, file=open("ResultONTID.txt", "w"))
    value = open("ResultONTID.txt", "r").read()
    resultONT = re.search(conditionONT, value)
    end = resultONT.span()[1]
    ontID = value[end:end+3].replace(" ", "")
    commandToSend(f"ont optical-alarm-profile {port} {ontID} profile-id 3")
    enter()
    commandToSend(f"ont alarm-policy {port} {ontID} policy-id 1")
    enter()
    if (deviceType[:6] == "bridge"):
        commandToSend(
            f"ont port native-vlan {port} {ontID} eth 1 vlan {provider}")
        enter()
        enter()
    commandToSend("quit")
    enter()
    return ontID


def addOnuService(spid, provider, slot, port, ontID, plan, commandToSend, enter, comm):
    command = f"""service-port {spid} vlan {provider} gpon 0/{slot}/{port} ont {ontID} gemport 14 multi-service user-vlan {provider} tag-transform transparent inbound traffic-table name {plan} outbound traffic-table name {plan}"""
    commandToSend(command)
    enter()
