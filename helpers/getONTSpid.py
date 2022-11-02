from helpers.outputDecoder import parser, decoder, check
from helpers.failHandler import failChecker

conditionSPID = "CTRL_C to break"
conditionQTY = "Total : "


def getOntSpid(comm, command, FRAME, SLOT, PORT, ID):
    command(f" display  service-port  port  {FRAME}/{SLOT}/{PORT}  ont  {ID}  |  include Total")
    valueQ = decoder(comm)
    fail = failChecker(valueQ)
    if fail == None:
        (_, eQ) = check(valueQ, conditionQTY).span()
        qty = int(valueQ[eQ : eQ + 2])
        command(f"display service-port port {FRAME}/{SLOT}/{PORT} ont {ID} | include gpon")
        value = decoder(comm)
        (_, e1) = check(value, conditionSPID).span()
        if qty == 2:
            spid1 = int(value[e1 : e1 + 10])
            spid2 = int(value[e1 + 87 : e1 + 92])
            return {"ttl": 2, "values": (spid1, spid2)}
        if qty == 1:
            spid = int(value[e1 : e1 + 10])
            return {"ttl": 1, "values": spid}
    else:
        return {"ttl": fail, "values": None}
