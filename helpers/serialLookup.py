from helpers.outputDecoder import parser,check,checkIter
from time import sleep

existingCond = (
    "-----------------------------------------------------------------------------"
)
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


def serialSearch(comm,command,SN):
  command(f"display ont info by-sn {SN} | no-more")
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
  (_, sDESC) = check(value, existing["DESC"]).span()
  (eDESC, _) = check(value, existing["LDC"]).span()
  (_, sCF) = check(value, existing["CF"]).span()
  (eCF, _) = check(value, existing["RE"]).span()
  FRAME = 0
  ID = value[eID : eID + 3].replace("\n", "")
  NAME = value[sDESC:eDESC].replace("\n", "")
  STATE = value[sCF:eCF].replace("\n", "")
  return(FRAME,SLOT,PORT,ID,NAME,STATE)