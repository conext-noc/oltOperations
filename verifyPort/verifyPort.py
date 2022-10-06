import re
import os
import csv
from helpers.csvParser import parser

condition = "-----------------------------------------------------------------------------"

def verifyPort(comm,command,enter):
  resp = input("Accion continua? [Y | N] : ")
  keep = True if resp == "Y" else  False
  while keep == True:
    SLOT = input("Ingrese slot de clientes : ")
    PORT = input("Ingrese puerto de los clientes : ")
    CLIENTS = input("Ingrese los ID de los clientes separados por espacios : ")
    same = True
    keep = True
    user_list = CLIENTS.split()
    for i in range(len(user_list)):
        user_list[i] = int(user_list[i])
    command(f"display ont info summary 0/{SLOT}/{PORT} | no-more")
    enter()
    if same == True:
      outputPort = comm.recv(65535)
      outputPort = outputPort.decode("ascii")
      print(outputPort, file=open(f"ResultPorts.txt", "w"))
      valuePort = open(f"ResultPorts.txt", "r").read()
      resultPort = []
      res = re.finditer(condition,valuePort)
      os.remove("ResultPorts.txt")
      for match in res:
        resultPort.append(match.span())

      (_,start) = resultPort[2]
      (end,_) = resultPort[3]
      data= re.sub(' +', ' ',valuePort[start+2:end]).replace(" ", ",")
      print(data, file=open(f"ResultClients.txt", "w"))
      f = open("ResultClients.txt")
      lines = f.readlines()
      f.close()
      f = open("ResultClients.txt", 'w')
      for line in lines:
          f.write(line[1:])
      f.close()
      valueClients = open(f"ResultClients.txt", "r").read()
      os.remove("ResultClients.txt")
      header = """id,status,lastUP,timeUp,lastDown,timeDown,cause
      """
      print(header + valueClients,file=open(f"ResultClients.csv", "w"))
      value = parser("ResultClients.csv")
      clients = []
      for client in value:
        for ID in CLIENTS:
          if client["id"] == ID:
            clients.append(client)

      with open(f'ResultClients.csv', 'w', newline='') as f:
            dict_writer = csv.DictWriter(f, keys)
            dict_writer.writeheader()
            dict_writer.writerows(data)
      preg = input("continuar? [Y | N] : ")
      keep = True if preg == "Y" else  False
    else:
      SLOT = input("Ingrese slot de clientes : ")
      PORT = input("Ingrese puerto de los clientes : ")
      CLIENTS = input("Ingrese los ID de los clientes separados por espacios : ")
      user_list = CLIENTS.split()
      for i in range(len(user_list)):
          user_list[i] = int(user_list[i])
      command(f"display ont info summary 0/{SLOT}/{PORT} | no-more")
      enter()
      same = True