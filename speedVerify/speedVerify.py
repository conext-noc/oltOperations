import re
import os
import time

upstream = "Up traffic \(kbps\)          : "
downstream = "Down traffic \(kbps\)        : "

def speedVerify(comm,command):
  speedUpArr = []
  speedDownArr = []
  SLOT = input("Ingrese slot de cliente : ")
  PORT = input("Ingrese puerto de cliente : ")
  ID = input("Ingrese el id del cliente : ")
  command(f"interface gpon 0/{SLOT}")
  for i in range(0,15):
    comm.send(f"display ont traffic {PORT} {ID}")
    time.sleep(5)
    outputSpeed = comm.recv(65535)
    outputSpeed = outputSpeed.decode("ascii")
    print(outputSpeed, file=open(f"Result{i}.txt", "w"))
    valueSpeed = open(f"Result{i}.txt", "r").read()
    resultUpSpeed = re.search(upstream, valueSpeed)
    endSpeed = resultUpSpeed.span()[1]
    upSpeed = int(valueSpeed[endSpeed:endSpeed+5])
    resultDownSpeed = re.search(downstream, valueSpeed)
    endSpeed = resultDownSpeed.span()[1]
    downSpeed = int(valueSpeed[endSpeed:endSpeed+5])
    speedUpArr.append(upSpeed)
    speedDownArr.append(downSpeed)
    os.remove(f"Result{i}.txt")
    i = i + 1
  command("quit")
  upLen = len(speedUpArr)
  upSum = sum(speedUpArr)
  upAVG = upSum / upLen
  downLen = len(speedDownArr)
  downSum = sum(speedDownArr)
  downAVG = downSum / downLen
  print(f"""
El consumo promedio del ONT es {upAVG} Kbps [UP] y {downAVG} Kbps [DOWN]
""")