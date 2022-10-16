from helpers.outputDecoder import parser, check, checkIter
from verifyReset.verifyReset import verifyWAN
from time import sleep

existingCond = (
    "-----------------------------------------------------------------------------"
)
newCond = "----------------------------------------------------------------------------"
newCondFSP = "F/S/P               : "
newCondSn = "Ont SN              : "
existing = {
    "FSP": "F/S/P                   : ",
    "LP": "Line profile name    : ",
    "SRV": "Service profile name : ",
    "ONTID": "ONT-ID                  : ",
    "CF": "Control flag            : ",
    "CS": "Config state",
    "RE": "Run state               : ",
    "DESC": "Description             : ",
    "LDC": "Last down cause         : ",
    "LDT": "Last down time          : ",
    "LUT": "Last up time            : ",
    "LDGT": "Last dying gasp time    : ",
}


def newLookup(comm, command, enter, olt):
    client = []
    command("display ont autofind all | no-more")
    enter()
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


def existingLookup(comm, command, enter, olt):
    lookupType = input("Buscar cliente por serial o por nombre [S | N] : ")
    if lookupType == "S":
        SN = input("Ingrese el Serial del Cliente a buscar : ")
        command(f"display ont info by-sn {SN} | no-more")
        enter()
        sleep(3)
        (val, regex) = parser(comm, existingCond, "m")
        (_, s) = regex[0]
        (e, _) = regex[len(regex) - 1]
        value = val[s:e]
        (_, eFSP) = check(value, existing["FSP"]).span()
        valFSP = value[eFSP : eFSP + 6].replace("\n", "")
        reFSP = checkIter(valFSP, "/")
        (_, eSLOT) = reFSP[0]
        (_, ePORT) = reFSP[1]
        SLOT = valFSP[eSLOT : eSLOT + 1].replace("\n", "")
        PORT = valFSP[ePORT : ePORT + 2].replace("\n", "")
        (_, eID) = check(value, existing["ONTID"]).span()
        (_, eLP) = check(value, existing["LP"]).span()
        (_, eSRV) = check(value, existing["SRV"]).span()
        (_, sDESC) = check(value, existing["DESC"]).span()
        (_, sCF) = check(value, existing["CF"]).span()
        (eCF, sRE) = check(value, existing["RE"]).span()
        (eRE, _) = check(value, existing["CS"]).span()
        (eDESC, sLDC) = check(value, existing["LDC"]).span()
        (eLDC, sLUT) = check(value, existing["LUT"]).span()
        (eLUT, sLDT) = check(value, existing["LDT"]).span()
        (eLDT, _) = check(value, existing["LDGT"]).span()
        FRAME = 0
        ID = value[eID : eID + 3].replace("\n", "")
        NAME = value[sDESC:eDESC].replace("\n", "")
        RUNSTATE = value[sRE:eRE].replace("\n", "")
        LDC = value[sLDC:eLDC].replace("\n", "")
        LDT = value[sLDT:eLDT].replace("\n", "")
        LUT = value[sLUT:eLUT].replace("\n", "")
        STATE = value[sCF:eCF].replace("\n", "")
        LP = value[eLP : eLP + 4].replace("\n", "")
        SRV = value[eSRV : eSRV + 4].replace("\n", "")
        VLAN = verifyWAN(comm, command, enter, SLOT, PORT, ID)

        print(
            f"""
FRAME             : {FRAME}
SLOT              : {SLOT}
PORT              : {PORT}
ID                : {ID}
NAME              : {NAME}
STATE             : {STATE}
RUN STATE         : {RUNSTATE}
VLAN              : {VLAN}
LAST DOWN TIME    : {LDT}
LAST DOWN CAUSE   : {LDC}
LAST UP TIME      : {LUT}
LINE PROFILE      : {LP}
SERVICE PROFILE   : {SRV}
"""
        )
    elif lookupType == "N":
        NAME = input("Ingrese el Nombre del Cliente a buscar : ")
        command(f'display ont info by-desc "{NAME}" | no-more')
        enter()
        sleep(3)
        (value, regex) = parser(comm, existingCond, "m")
        (_, s) = regex[0]
        (e, _) = regex[len(regex) - 1]
        print(value[s:e])
    else:
        print(f'la opcion "{lookupType}" no existe')
