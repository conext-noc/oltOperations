from helpers.outputDecoder import parser, checkIter
from time import sleep

existingCond = (
    "-----------------------------------------------------------------------------"
)
newCond = "----------------------------------------------------------------------------"
newCondFSP = "F/S/P               : "
newCondSn = "Ont SN              : "


def newLookup(comm, command, enter, olt):
    command("display ont autofind all | no-more")
    enter()
    (value, regex) = parser(comm, newCond, "m")
    (_, s) = regex[0]
    (e, _) = regex[len(regex) - 1]
    result = value[s:e]
    valuesFSP = checkIter(result, newCondFSP)
    valuesSN = checkIter(result, newCondSn)
    print("| {:^10} | {:^25} |".format("F/S/P", "SN"))
    for (fsp, sn) in zip(valuesFSP, valuesSN):
        (_, eFSP) = fsp
        (_, eSN) = sn
        FSP = result[eFSP : eFSP + 6].replace(" ", "").replace("\n", "")
        SN = result[eSN : eSN + 16].replace(" ", "")
        print("| {:^10} | {:^25} |".format(FSP, SN))


def existingLookup(comm, command, enter, olt):
    lookupType = input("Buscar cliente por serial o por nombre [S | N] : ")
    if lookupType == "S":
        SN = input("Ingrese el Serial del Cliente a buscar : ")
        command(f"display ont info by-sn {SN} | no-more")
        enter()
        sleep(3)
        (value, _) = parser(comm, existingCond, "m")
        print(value)

    elif lookupType == "N":
        NAME = input("Ingrese el Nombre del Cliente a buscar : ")
        command(f'display ont info by-desc "{NAME}" | no-more')
        enter()
        (value, regex) = parser(comm, existingCond, "m")
        (_, s) = regex[0]
        (e, _) = regex[len(regex) - 1]
        print(value[s:e])
    else:
        print(f'la opcion "{lookupType}" no existe')
