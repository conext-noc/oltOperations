from helpers.outputDecoder import parser, decoder, check
from helpers.failHandler import failChecker

conditionSPID = "CTRL_C to break"
conditionQTY = "Total : "


def getOntSpid(comm, command, FRAME, SLOT, PORT, ID):
    command(
        f" display  service-port  port  {FRAME}/{SLOT}/{PORT}  ont  {ID}  |  include Total"
    )
    (value, re) = parser(comm, conditionQTY, "s")
    fail = failChecker(value)
    if fail == None:
        end = re.span()[1]
        qty = int(value[end : end + 2])
        command(
            f"display service-port port {FRAME}/{SLOT}/{PORT} ont {ID} | include gpon"
        )
        (value, re1) = parser(comm, conditionSPID, "s")
        end1 = re1.span()[1]
        if qty == 2:
            spid1 = int(value[end1 : end1 + 10])
            spid2 = int(value[end1 + 87 : end1 + 92])
            return {"ttl": 2, "values": (spid1, spid2)}
        if qty == 1:
            spid = int(value[end1 : end1 + 10])
            return {"ttl": 1, "values": spid}
    else:
        return {"ttl": fail, "values": None}
