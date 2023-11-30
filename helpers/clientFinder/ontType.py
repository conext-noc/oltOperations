from helpers.utils.decoder import check, decoder
from helpers.failHandler.fail import failChecker
import re

ontTypeStart = "OntProductDescription    : "
ontTypeEnd = "GPON"
vendorId = r"Vendor-ID\s*:\s*(\w+)"

def typeCheck(comm,command,data):
  ONT_TYPE = None
  FAIL = None
  command(f"  interface  gpon  {data['frame']}/{data['slot']}  ")
  command(f"  display  ont  version  {data['port']}  {data['onu_id']}  ")
  command("quit")
  value = decoder(comm)
  FAIL = failChecker(value)
  if(FAIL == None):
    matches = re.findall(vendorId, value)
    if matches:
        if matches[0].strip() == "BDCM":
            ONT_TYPE = matches[0].strip()
        else:
            (_,tS) = check(value,ontTypeStart).span()
            (tE,_) = check(value, ontTypeEnd).span()
            ONT_TYPE = value[tS:tE]
        
    return ONT_TYPE
  else:
    return ONT_TYPE