from helpers.outputDecoder import parser

ip = "IPv4 address               : "

def verifyReset(comm,command,enter):
  SLOT = input("Ingrese slot de cliente : ")
  PORT = input("Ingrese puerto de cliente : ")
  ID = input("Ingrese el id del cliente : ")
  NAME = input("Ingrese nombre del cliente : ")

  command(f"interface gpon 0/{SLOT}")
  enter()
  command(f"display ont wan-info {PORT} {ID} | include \"IPv4 address\" ")
  enter()

  (value,re) = parser(comm,ip,"s")
  if(re != None):
    endIp = re.span()[1]
    IP = value[endIp:endIp+15].replace("\n","").replace(" ","")
    print(f"El cliente {NAME} tiene la IP : {IP}")
  else:
    print(f"El cliente {NAME} tiene reset")
  