from helpers.getONTSpid import getSPIDChange

providerMap = {
    "INTER": 1101,
    "VNET": 1102,
    "PUBLICAS": 1104
}

def providerChange(comm,command,enter,olt):
  SLOT = input("Ingrese slot de cliente : ")
  PORT = input("Ingrese puerto de cliente : ")
  ID = input("Ingrese el id del cliente : ")
  PROVIDER = input("Ingrese proevedor de cliente [INTER | VNET] : ")
  NAME = input("Ingrese nombre del cliente : ")
  PLAN = input("Ingrese plan de cliente : ")

  result = getSPIDChange(comm, command, enter, SLOT,PORT,ID)
  if(result["ttl"] == 1):
    spid = result["values"]
    prov = providerMap[PROVIDER]
    command(f"undo service-port {spid}")
    enter()
    command(f"""service-PORT {spid} vlan {prov} gpon 0/{SLOT}/{PORT} ont {ID} gemport 14 multi-service user-vlan {prov} tag-transform transparent inbound traffic-table name {PLAN} outbound traffic-table name {PLAN}""")
    enter()
    isBridge = input("ONT es un bridge? [Y | N] : ")
    if(isBridge == "Y"):
      command(f"interface gpon 0/{SLOT}")
      enter()
      command(f"ont port native-vlan {PORT} {ID} eth 1 vlan {prov}")
      enter()
      command("quit")
      enter()
    print(f"El Cliente {NAME} 0/{SLOT}/{PORT}/{ID} OLT {olt} ha sido cambiado al proveedor {PROVIDER}")
  else:
    spid1 = result["values"][0]
    spid2 = result["values"][1]
    prov = providerMap[PROVIDER]
    command(f"undo service-port {spid1}")
    enter()
    command(f"undo service-port {spid2}")
    enter()
    command(f"""service-PORT {spid1} vlan {prov} gpon 0/{SLOT}/{PORT} ont {ID} gemport 14 multi-service user-vlan {prov} tag-transform transparent inbound traffic-table name {PLAN} outbound traffic-table name {PLAN}""")
    enter()
    command(f"""service-PORT {spid2} vlan {prov} gpon 0/{SLOT}/{PORT} ont {ID} gemport 14 multi-service user-vlan {prov} tag-transform transparent inbound traffic-table name {PLAN} outbound traffic-table name {PLAN}""")
    enter()

    isBridge = input("ONT es un bridge? [Y | N] : ")
    if(isBridge == "Y"):
      command(f"interface gpon 0/{SLOT}")
      enter()
      command(f"ont port native-vlan {PORT} {ID} eth 1 vlan {prov}")
      enter()
      command("quit")
      enter()
    print(f"El Cliente {NAME} 0/{SLOT}/{PORT}/{ID} OLT {olt} ha sido cambiado al proveedor {PROVIDER}")