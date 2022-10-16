from helpers.ontCheck import verifyValues
from helpers.outputDecoder import parser, check
from helpers.calcAvg import avg
import time

upstream = "Up traffic \(kbps\)          : "
downstream = "Down traffic \(kbps\)        : "


def valueVerify(comm, command, enter):
    speedUpArr = []
    speedDownArr = []
    SLOT = input("Ingrese slot de cliente : ")
    PORT = input("Ingrese puerto de cliente : ")
    ID = input("Ingrese el id del cliente : ")
    (TEMP, PWR) = verifyValues(comm, command, enter, SLOT, PORT, ID)
    command(f"interface gpon 0/{SLOT}")
    enter()
    for i in range(0, 5):
        comm.send(f"display ont traffic {PORT} {ID}")
        enter()
        time.sleep(5)
        (value, reUp) = parser(comm, upstream, "s")
        reDn = check(value, downstream)
        (_, eU) = reUp.span()
        (_, eD) = reDn.span()
        upSpeed = int(value[eU : eU + 5])
        downSpeed = int(value[eD : eD + 5])
        speedUpArr.append(upSpeed)
        speedDownArr.append(downSpeed)
        i += 1
    command("quit")
    enter()
    (upAVG, downAVG) = avg(speedUpArr, speedDownArr)
    print(
        f"""
La potencia del ONT es : {PWR}
La temperatura es : {TEMP}
El consumo promedio del ONT es {upAVG} Kbps [UP] y {downAVG} Kbps [DOWN]
"""
    )
