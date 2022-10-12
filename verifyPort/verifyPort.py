import re
import os
from helpers.outputDecoder import parser as outputParser, decoder
from helpers.csvParser import parser

condition = "-----------------------------------------------------------------------------"

def verifyPort(comm,command,enter):
  types = [{"name":"status","start":2,"end":3, "header":"""id,status,lastUP,timeUp,lastDown,timeDown,cause
      """},{"name":"names","start":4,"end":5, "header": """id,sn,type,distance,Rx/Tx power,NAME1,NAME2,NAME3,NAME4
      """}]
  keep = True
  while keep == True:
    SLOT = input("Ingrese slot de clientes : ")
    PORT = input("Ingrese puerto de los clientes : ")
    keep = True
    command(f"display ont info summary 0/{SLOT}/{PORT} | no-more")
    enter()
    (valueSSH,result) = outputParser(comm, condition, "m")

    for tp in types:
      start = tp["start"]
      end = tp["end"]
      name = tp["name"]
      header = tp["header"]
      (_,s) = result[start]
      (e,_) = result[end]
      data = re.sub(' +', ' ',valueSSH[s+2:e]).replace(" ", ",")
      print(data, file=open(f"{name}.txt", "w"))
      f = open(f"{name}.txt")
      lines = f.readlines()
      f.close()
      f = open(f"{name}.txt", 'w')
      for line in lines:
          f.write(line[1:])
      f.close()
      valueRES = open(f"{name}.txt", "r").read()
      os.remove(f"{name}.txt")
      print(header + valueRES,file=open(f"{name}.txt", "w"))
      value = open(f"{name}.txt", "r").read()
      os.remove(f"{name}.txt")
      print(value,file=open(f"{name}Result.csv", "w"))

    valueStatus = parser("statusResult.csv")
    valueNames = parser("namesResult.csv")

    print("| {:^5} | {:^25} | {:^10} | {:^15} |{:^10} |".format("ID","NAME","STATUS","CAUSE","TIME"))
    for (status, names) in zip(valueStatus,valueNames):
      if(status["id"] == names["id"]):
        name = " "
        ID = names["id"].replace(" ","")
        STATUS = status["status"]
        CAUSE = status["cause"]
        TIME = status["timeDown"]
        for i in range(1,5):
          if(names[f"NAME{i}"] != None):
            name = name + names[f"NAME{i}"] + " "
        print("| {:^5} | {:^25} | {:^10} | {:^15} |{:^10} |".format(ID,name,STATUS,CAUSE,TIME))
    os.remove("statusResult.csv")
    os.remove("namesResult.csv")
    preg = input("continuar? [Y | N] : ")
    keep = True if preg == "Y" else  False