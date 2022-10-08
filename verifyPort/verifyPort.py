import re
import os
import csv
import itertools
from helpers.csvParser import parser

condition = "-----------------------------------------------------------------------------"

def verifyPort(comm,command,enter):
  types = [{"name":"status","start":2,"end":3, "header":"""id,status,lastUP,timeUp,lastDown,timeDown,cause
      """},{"name":"names","start":4,"end":5, "header": """id,sn,type,distance,Rx/Tx power,NAME1,NAME2,NAME3,NAME4
      """}]
  resp = input("Accion continua? [Y | N] : ")
  keep = True if resp == "Y" else  False
  while keep == True:
    SLOT = input("Ingrese slot de clientes : ")
    PORT = input("Ingrese puerto de los clientes : ")
    same = True
    keep = True
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

      for tp in types:
        start = tp["start"]
        end = tp["end"]
        name = tp["name"]
        header = tp["header"]
        (_,s) = resultPort[start]
        (e,_) = resultPort[end]
        data = re.sub(' +', ' ',valuePort[s+2:e]).replace(" ", ",")
        print(data, file=open(f"{name}.txt", "w"))
        f = open(f"{name}.txt")
        lines = f.readlines()
        f.close()
        f = open(f"{name}.txt", 'w')
        for line in lines:
            f.write(line[1:])
        f.close()
        value = open(f"{name}.txt", "r").read()
        os.remove(f"{name}.txt")
        print(header + value,file=open(f"{name}Result.csv", "w"))
      
      valueStatus = parser("statusResult.csv")
      valueNames = parser("namesResult.csv")

      print(f"ID   NAME                STATUS    CAUSE    TIME")
      for (status, names) in zip(valueStatus,valueNames):
        if(status["id"] == names["id"]):
          name = " "
          ID = names["id"]
          STATUS = status["status"]
          CAUSE = status["cause"]
          TIME = status["timeDown"]
          for i in range(1,5):
            if(names[f"NAME{i}"] != None):
              name = name + names[f"NAME{i}"]
          print(f"{ID}    {name}    {STATUS}    {CAUSE}    {TIME}")
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