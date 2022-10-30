from helpers.getONTSpid import getOntSpid

def delete(comm,command, OLT):
  SLOT = input("Ingrese slot de cliente : ")
  PORT = input("Ingrese puerto de cliente : ")
  ID = input("Ingrese el id del cliente : ")
  NAME = input("Ingrese nombre del cliente : ")
  result = getOntSpid(comm, command, SLOT,PORT,ID)
  if(result["ttl"] == 2):
    spid1=result["values"][0]
    spid2=result["values"][1]
    command(f"undo service-port {spid1}")
    command(f"undo service-port {spid2}")
  if(result["ttl"] == 1):
    spid = result["values"]
    command(f"undo service-port {spid}")
  command(f"interface gpon 0/{SLOT}")
  command(f"ont delete {PORT} {ID}")
  command("quit")
  print(f"{NAME} 0/{SLOT}/{PORT}/{ID} de OLT {OLT} ha sido eliminado")
