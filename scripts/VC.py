from helpers.clientFinder.dataLookup import dataLookup
from helpers.clientFinder.lookup import lookup
from helpers.failHandler.fail import failChecker
from helpers.utils.decoder import check, checkIter, decoder
from helpers.utils.display import display
from helpers.utils.printer import colorFormatter, inp, log
from helpers.info.regexConditions import speed
from time import sleep


def verifyTraffic(comm,command,quit,olt, action):
    """
    comm        :   ssh connection handler [class]
    command     :   sends ssh commands [func]
    quit        :   terminates the ssh connection [func]
    olt         :   defines the selected olt [var:str]
    action      :   defines the type of lookup/action of the client [var:str]
    
    This module monitors the real time traffic of a given client
    """
    speedUpArr = []
    speedDownArr = []
    lookupType = inp("Buscar cliente por serial o por Datos (F/S/P/ID) [S | D] : ")
    data = lookup(comm, command, olt, lookupType)
    if data["fail"] != None:
        log(colorFormatter(data["fail"], "fail"))
        quit()
        return
    proceed = display(data,"A")
    if not proceed:
        log(colorFormatter("Cancelando...", "warning"))
        quit()
        return
    command(f"interface gpon {data['frame']}/{data['slot']}")
    for i in range(0, 10):
        command(f"display ont traffic {data['port']} {data['onu_id']}")
        sleep(5)
        outputSpeed = decoder(comm)
        fail = failChecker(outputSpeed)
        if fail == None:
            (_, sUpSpeed) = check(outputSpeed, speed["up"]).span()
            (eUpSpeed, sDownSpeed) = check(outputSpeed, speed["down"]).span()
            (eDownSpeed, _) = checkIter(outputSpeed, speed["cond"])[2]
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