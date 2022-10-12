from helpers.outputDecoder import parser

conditionSPID = "CTRL_C to break"
conditionQTY = "Total : "


def getSPIDChange(comm, command, enter, SLOT, PORT, ID):
    command(
        f"display service-port port 0/{SLOT}/{PORT} ont {ID} | include Total")
    enter()
    (value,re) = parser(comm,conditionQTY,"s")
    end = re.span()[1]
    qty = int(value[end:end+2])
    command(
        f"display service-port port 0/{SLOT}/{PORT} ont {ID} | include gpon")
    enter()
    (value,re1) = parser(comm,conditionSPID,"s")
    end1 = re1.span()[1]
    if (qty == 2):
        spid1 = int(value[end1:end1+10])
        spid2 = int(value[end1+87:end1+92])
        return {"ttl": 2, "values": (spid1, spid2)}
    if (qty == 1):
        spid = int(value[end1:end1+10])
        return {"ttl": 1, "values": spid}
