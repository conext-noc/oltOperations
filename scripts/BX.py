from helpers.failHandler import failChecker
from helpers.serialLookup import serialSearch
from helpers.formatter import colorFormatter
from helpers.outputDecoder import parser, check
from helpers.opticalCheck import opticalValues
from helpers.getWanData import wan
from time import sleep
import re
from helpers.clientDataLookup import lookup


condition = "-----------------------------------------------------------------------------"
newCond = "----------------------------------------------------------------------------"
newCondFSP = "F/S/P               : "
newCondSn = "Ont SN              : "


def newLookup(comm, command, olt):
    client = []
    command("  display  ont  autofind  all  |  no-more  ")
    sleep(5)
    (value, regex) = parser(comm, newCond, "m")
    for ont in range(len(regex) - 1):
        (_, s) = regex[ont]
        (e, _) = regex[ont + 1]
        result = value[s:e]
        (_, eFSP) = check(result, newCondFSP).span()
        (_, eSN) = check(result, newCondSn).span()
        aSN = result[eSN : eSN + 16].replace("\n", "").replace(" ", "")
        aFSP = result[eFSP : eFSP + 6].replace("\n", "").replace(" ", "")
        client.append({"FSP": aFSP, "SN": aSN, "IDX": ont})
    print("| {:^3} | {:^6} | {:^16} |".format("IDX", "F/S/P", "SN"))
    for ont in client:
        FSP = ont["FSP"].replace(" ", "")
        SN = ont["SN"].replace(" ", "")
        IDX = ont["IDX"] + 1
        print("| {:^3} | {:^6} | {:^16} |".format(IDX, FSP, SN))


def existingLookup(comm, command, olt):
    lookupType = input("Buscar cliente por serial, por nombre o por Datos de OLT [S | N | D] : ").upper()
    data = lookup(comm, command, olt, lookupType)
    if data["fail"] == None:
        if lookupType == "S" or lookupType == "D":
            str1 = f"""
    FRAME               :   {data["frame"]}
    SLOT                :   {data["slot"]}
    PORT                :   {data["port"]}
    ID                  :   {data["id"]}
    NAME                :   {data["name"]}
    STATE               :   {data["state"]}
    IP                  :   {data["ipAdd"]}
    TEMPERATURA         :   {data["temp"]}
    POTENCIA            :   {data["pwr"]}
                """
            str2 = ""
            for idx, wanData in enumerate(data["wan"]):
                str2 += f"""
    VLAN_{idx}              :   {wanData["VLAN"]}
    PLAN_{idx}              :   {wanData["PLAN"]}
    SPID_{idx}              :   {wanData["SPID"]}
                """
            res = str1 + str2
            res = colorFormatter(res, "ok")
            print(res)
        elif lookupType == "N":
            command(f'display ont info by-desc "{data["name"]}" | no-more')
            sleep(3)
            (value, regex) = parser(comm, condition, "m")
            fail = failChecker(value)
            if fail == None:
                (_, s) = regex[0]
                (e, _) = regex[len(regex) - 1]
                print(value[s:e])
            else:
                fail = colorFormatter(fail, "fail")
                print(fail)
