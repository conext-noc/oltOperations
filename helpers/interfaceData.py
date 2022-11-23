from helpers.outputDecoder import check
import pandas as pd
from helpers.tableConverter import toDict
condStart = "InUti/OutUti: input utility/output utility"
condEnd  = "NULL0"
header = "Interface,PHY,Protocol,InUti,OutUti,inErrors,outErrors\n"

def intFormatter(data, infc):
  (_,s) = check(data, condStart).span()
  (e,_) = check(data, condEnd).span()
  value = toDict(header,data[s:e])
  result = list(filter(lambda interface: interface['Interface'] == infc, value))[0]
  return result