import re
import os

conditionTemp = "Temperature\(C\)                         : "
conditionPwr = "Rx optical power\(dBm\)                  : "

def verifyValues(comm, command, enter, SLOT, PORT, ID):
    enter()
    outputX = comm.recv(65535)
    outputX = outputX.decode("ascii")
    command(f"interface gpon 0/{SLOT}")
    enter()

    command(
        f"""display ont optical-info {PORT} {ID}| include Temperature""")
    enter()
    outputTemp = comm.recv(65535)
    outputTemp = outputTemp.decode("ascii")
    print(outputTemp, file=open("ResultTemp.txt", "w"))
    valueTemp = open("ResultTemp.txt", "r").read()
    resultTemp = re.search(conditionTemp, valueTemp)
    endTemp = resultTemp.span()[1]
    temp = valueTemp[endTemp:endTemp+4]
    os.remove("ResultTemp.txt")

    command(f"display ont optical-info {PORT} {ID} | include Rx")
    enter()
    outputPwr = comm.recv(65535)
    outputPwr = outputPwr.decode("ascii")
    print(outputPwr, file=open("ResultPwr.txt", "w"))
    valuePwr = open("ResultPwr.txt", "r").read()
    resultPwr = re.search(conditionPwr, valuePwr)
    endPwr = resultPwr.span()[1]
    pwr = valuePwr[endPwr:endPwr+6]
    os.remove("ResultPwr.txt")

    command("quit")
    enter()
    return (temp, pwr)
