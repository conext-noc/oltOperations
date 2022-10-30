from helpers.getONTSpid import getOntSpid

def newPlan(comm, command, olt):
    SLOT = input("Ingrese slot de cliente : ")
    PORT = input("Ingrese puerto de cliente : ")
    ID = input("Ingrese el id del cliente : ")
    NAME = input("Ingrese nombre del cliente : ")
    PLAN = input("Ingrese plan de cliente : ")
    result = getOntSpid(comm, command, SLOT, PORT, ID)
    if (result["ttl"] == 2):
        spid1 = result["values"][0]
        spid2 = result["values"][1]
        command(
            f"service-port {spid1} inbound traffic-table name {PLAN} outbound traffic-table name {PLAN}")
        command(
            f"service-port {spid2} inbound traffic-table name {PLAN} outbound traffic-table name {PLAN}")
    if (result["ttl"] == 1):
        spid = result["values"]
        command(
            f"service-port {spid} inbound traffic-table name {PLAN} outbound traffic-table name {PLAN}")
    print(
        f"El Cliente {NAME} 0/{SLOT}/{PORT}/{ID} OLT {olt} ha sido cambiado al plan {PLAN}")
