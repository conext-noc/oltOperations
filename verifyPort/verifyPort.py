import re
import os
from time import sleep
from helpers.outputDecoder import parser as outputParser, decoder
from helpers.csvParser import parser

condition = (
    "------------------------------------------------------------------------------"
)


def verifyPort(comm, command, enter):
    types = [
        {
            "name": "status",
            "start": 2,
            "end": 3,
            "header": "id,status,lastUP,timeUp,lastDown,timeDown,cause,NA\n",
        },
        {
            "name": "names",
            "start": 4,
            "end": 5,
            "header": "id,sn,type,distance,Rx/Tx power,NAME1,NAME2,NAME3,NAME4,NAME5\n",
        },
    ]
    keep = True
    while keep == True:
        SLOT = input("Ingrese slot de clientes : ")
        PORT = input("Ingrese puerto de los clientes : ")
        keep = True
        command(f"display ont info summary 0/{SLOT}/{PORT} | no-more")
        enter()
        sleep(3)
        (valueSSH, result) = outputParser(comm, condition, "m")

        for tp in types:
            start = tp["start"]
            end = tp["end"]
            name = tp["name"]
            header = tp["header"]
            (_, s) = result[start]
            (e, _) = result[end]
            data = re.sub(" +", " ", valueSSH[s:e]).replace(" ", ",")
            print(data, file=open(f"{name}.txt", "w"))
            f = open(f"{name}.txt")
            lines = f.readlines()
            f.close()
            f = open(f"{name}.txt", "w")
            for line in lines:
                f.write(line[1:].replace(" +", ""))
            f.close()
            valueRES = open(f"{name}.txt", "r").read().replace(" +", "")
            os.remove(f"{name}.txt")
            print(header + valueRES, file=open(f"{name}.txt", "w"))
            value = open(f"{name}.txt", "r").read().replace(" +", "")
            os.remove(f"{name}.txt")
            print(value, file=open(f"{name}Result.csv", "w"))

        valueStatus = parser("statusResult.csv")
        valueNames = parser("namesResult.csv")

        print(
            "| {:^5} | {:^25} | {:^10} | {:^15} |{:^10} |".format(
                "ID", "NAME", "STATUS", "CAUSE", "TIME"
            )
        )
        for (status, names) in zip(valueStatus, valueNames):
            if status["id"] == names["id"]:
                ID = status["id"]
                STATUS = status["status"]
                CAUSE = status["cause"]
                TIME = status["timeDown"]
                NAME1 = str(names["NAME1"]) if str(names["NAME1"]) != "nan" else ""
                NAME2 = str(names["NAME2"]) if str(names["NAME2"]) != "nan" else ""
                NAME3 = str(names["NAME3"]) if str(names["NAME3"]) != "nan" else ""
                NAME4 = str(names["NAME4"]) if str(names["NAME4"]) != "nan" else ""
                NAME5 = str(names["NAME5"]) if str(names["NAME5"]) != "nan" else ""
                name = NAME1 + " " + NAME2 + " " + NAME3 + " " + NAME4 + " " + NAME5
                print(
                    "| {:^5} | {:^25} | {:^10} | {:^15} |{:^10} |".format(
                        ID, name, STATUS, CAUSE, TIME
                    )
                )
        os.remove("statusResult.csv")
        os.remove("namesResult.csv")
        preg = input("continuar? [Y | N] : ")
        keep = True if preg == "Y" else False
