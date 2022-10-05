import re
import os

conditionSPID = "CTRL_C to break"
conditionQTY = "Total : "

def getSPIDChange(comm,command,enter,SLOT,PORT,ID):
    command(f"display service-port port 0/{SLOT}/{PORT} ont {ID} | include Total")
    enter()
    output = comm.recv(65535)
    output = output.decode("ascii")
    print(output, file=open("ResultSPIDQTY.txt", "w"))
    value = open("ResultSPIDQTY.txt", "r").read()
    result = re.search(conditionQTY, value)
    end = result.span()[1]
    qty = int(value[end:end+2])
    os.remove("ResultSPIDQTY.txt")
    command(f"display service-port port 0/{SLOT}/{PORT} ont {ID} | include gpon")
    enter()
    output = comm.recv(65535)
    output = output.decode("ascii")
    print(output, file=open("ResultSPID.txt", "w"))
    value = open("ResultSPID.txt", "r").read()
    result1 = re.search(conditionSPID, value)
    end1 = result1.span()[1]
    os.remove("ResultSPID.txt")
    if(qty == 2):
        spid1 = int(value[end1:end1+10])
        spid2 = int(value[end1+87:end1+92])
        return {"ttl": 2, "values": (spid1,spid2)}
    if(qty == 1):
        spid = int(value[end1:end1+10])
        return {"ttl": 1, "values": spid}
    # return qty
