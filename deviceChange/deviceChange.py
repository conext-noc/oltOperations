def deviceChange(comm,command,enter, OLT):
  SLOT = input("Ingrese slot de cliente : ")
  PORT = input("Ingrese puerto de cliente : ")
  ID = input("Ingrese el id del cliente : ")
  NAME = input("Ingrese nombre del cliente : ")
  SN = input("Ingrese el nuevo ont del cliente : ")
  command(f"interface gpon 0/{SLOT}")
  enter()
  command(f"ont modify {PORT} {ID} sn {SN}")
  enter()
  print(f"Al Cliente {NAME} 0/{SLOT}/{PORT}/{ID} OLT {OLT} se ha sido cambiado el ont a {SN} satisfactoriamente")
  return ""