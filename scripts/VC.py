import os
import time
from helpers.outputDecoder import decoder, check, checkIter
from helpers.failHandler import failChecker
from helpers.printer import inp, log

upstream = "Up traffic \(kbps\)          : "
downstream = "Down traffic \(kbps\)        : "
endCond = "----------------------------------------------------------------"


def speedVerify(comm, command,quit):
    speedUpArr = []
    speedDownArr = []
    FRAME = inp("Ingrese frame de cliente : ").upper()
    SLOT = inp("Ingrese slot de cliente : ").upper()
    PORT = inp("Ingrese puerto de cliente : ").upper()
    ID = inp("Ingrese el id del cliente : ").upper()
    command(f"display ont info {FRAME} {SLOT} {PORT} {ID} | no-more")
    time.sleep(3)
    value = decoder(comm)
    fail = failChecker(value)
    if fail == None:
        (_, sDESC) = check(value, "Description             : ").span()
        (eDESC, _) = check(value, "Last down cause         : ").span()
        NAME = value[sDESC:eDESC].replace("\n", "")
        log(
            f"""
  NOMBRE              :   {NAME}
  FRAME               :   {FRAME}
  SLOT                :   {SLOT}
  PORT                :   {PORT}
  ID                  :   {ID}"""
        )
    command(f"interface gpon {FRAME}/{SLOT}")
    for i in range(0, 10):
        command(f"display ont traffic {PORT} {ID}")
        time.sleep(5)
        outputSpeed = decoder(comm)
        fail = failChecker(outputSpeed)
        if fail == None:
            (_, sUpSpeed) = check(outputSpeed, upstream).span()
            (eUpSpeed, sDownSpeed) = check(outputSpeed, downstream).span()
            (eDownSpeed, _) = checkIter(outputSpeed, endCond)[2]
            upSpeed = int(outputSpeed[sUpSpeed:eUpSpeed])
            downSpeed = int(outputSpeed[sDownSpeed:eDownSpeed])
            speedUpArr.append(upSpeed)
            speedDownArr.append(downSpeed)
        else:
            speedUpArr.append(0)
            speedDownArr.append(0)
        i = i + 1
    command("quit")
    upLen = len(speedUpArr)
    upSum = sum(speedUpArr)
    upAVG = upSum / upLen
    downLen = len(speedDownArr)
    downSum = sum(speedDownArr)
    downAVG = downSum / downLen
    log(
        f"""
El consumo promedio del ONT es {upAVG} Kbps [UP] y {downAVG} Kbps [DOWN]
"""
    )
    quit()
