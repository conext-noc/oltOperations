import re
import os

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

  outputIp = comm.recv(65535)
  outputIp = outputIp.decode("ascii")
  print(outputIp, file=open(f"ResultIP.txt", "w"))
  valueIp = open("ResultIP.txt", "r").read()
  resultIp = re.search(ip, valueIp)
  os.remove("ResultIP.txt")
  if(resultIp != None):
    endIp = resultIp.span()[1]
    IP = valueIp[endIp:endIp+15].replace("\n","").replace(" ","")
    print(f"El cliente {NAME} tiene la IP : {IP}")
  else:
    print(f"El cliente {NAME} tiene reset")
  