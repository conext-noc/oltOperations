import re
import os

conditionONT = """ONTID :"""

def addONU(comm, command, enter, SLOT, PORT,SN, PROVIDER, NAME, SRV, LP):
    command(f"interface gpon 0/{SLOT}")
    enter()
    command(f"ont add {PORT} sn-auth {SN} omci ont-lineprofile-name {LP} ont-srvprofile-name {SRV}  desc \"{NAME}\" ")
    enter()
    output = comm.recv(65535)
    output = output.decode("ascii")
    print(output, file=open("ResultONTID.txt", "w"))
    value = open("ResultONTID.txt", "r").read()
    resultONT = re.search(conditionONT, value)
    end = resultONT.span()[1]
    ID = value[end:end+3].replace(" ", "")
    os.remove("ResultONTID.txt")
    command(f"ont optical-alarm-profile {PORT} {ID} profile-id 3")
    enter()
    command(f"ont alarm-policy {PORT} {ID} policy-id 1")
    enter()
    addVlan = input("Se agregara vlan al puerto? (es bridge) [Y/N] : ")
    if(addVlan == "Y"):
        command(f"ont PORT native-vlan {PORT} {ID} eth 1 vlan {PROVIDER}")
        enter()
    command("quit")
    enter()
    return ID


def addOnuService(command, enter, SPID, PROVIDER, SLOT, PORT, ID, PLAN):
    command(f"""service-PORT {SPID} vlan {PROVIDER} gpon 0/{SLOT}/{PORT} ont {ID} gemport 14 multi-service user-vlan {PROVIDER} tag-transform transparent inbound traffic-table name {PLAN} outbound traffic-table name {PLAN}""")
    enter()
