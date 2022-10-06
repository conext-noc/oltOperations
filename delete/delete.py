from helpers.getONTSpid import getSPIDChange

def delete(comm,command,enter, OLT):
  SLOT = input("Ingrese slot de cliente : ")
  PORT = input("Ingrese puerto de cliente : ")
  ID = input("Ingrese el id del cliente : ")
  NAME = input("Ingrese nombre del cliente : ")
  result = getSPIDChange(comm, command, enter, SLOT,PORT,ID)
  if(result["ttl"] == 2):
    spid1=result["values"][0]
    spid2=result["values"][1]
    command(f"undo service-port {spid1}")
    enter()
    command(f"undo service-port {spid2}")
    enter()
  if(result["ttl"] == 1):
    spid = result["values"]
    command(f"undo service-port {spid}")
    enter()
  command(f"interface gpon 0/{SLOT}")
  enter()
  command(f"ont delete {PORT} {ID}")
  enter()
  command("quit")
  enter()
  print(f"{NAME} 0/{SLOT}/{PORT}/{ID} de OLT {OLT} ha sido eliminado")
