import re

conditionTemp = "Temperature\(C\)                         : "
conditionPwr = "Rx optical power\(dBm\)                  : "


def verifyValues(comm, slot, port, onuId, commandToSend, enter):
    commandToSend("enable")
    commandToSend("config")
    enter()
    outputX = comm.recv(65535)
    outputX = outputX.decode("ascii")
    commandToSend(f"interface gpon 0/{slot}")
    enter()

    commandToSend(
        f"display ont optical-info {port} {onuId} | include Temperature")
    enter()
    outputTemp = comm.recv(65535)
    outputTemp = outputTemp.decode("ascii")
    print(outputTemp, file=open("ResultTemp.txt", "w"))
    valueTemp = open("ResultTemp.txt", "r").read()
    resultTemp = re.search(conditionTemp, valueTemp)
    endTemp = resultTemp.span()[1]
    temp = valueTemp[endTemp:endTemp+4]

    commandToSend(f"display ont optical-info {port} {onuId} | include Rx")
    enter()
    outputPwr = comm.recv(65535)
    outputPwr = outputPwr.decode("ascii")
    print(outputPwr, file=open("ResultPwr.txt", "w"))
    valuePwr = open("ResultPwr.txt", "r").read()
    resultPwr = re.search(conditionPwr, valuePwr)
    endPwr = resultPwr.span()[1]
    pwr = valuePwr[endPwr:endPwr+6]

    return (temp, pwr)
