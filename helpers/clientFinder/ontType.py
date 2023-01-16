from helpers.utils.decoder import check, decoder
from helpers.failHandler.fail import failChecker

ontTypeStart = "OntProductDescription    : "
ontTypeEnd = "GPON"

def typeCheck(comm,command,data):
  ONT_TYPE = None
  FAIL = None
  command(f"  interface  gpon  {data['frame']}/{data['slot']}  ")
  command(f"  display  ont  version  {data['port']}  {data['onu_id']}  ")
  command("quit")
  value = decoder(comm)
  FAIL = failChecker(value)
  if(FAIL == None):
    (_,tS) = check(value,ontTypeStart).span()
    (tE,_) = check(value, ontTypeEnd).span()
    ONT_TYPE = value[tS:tE]
    return ONT_TYPE
  else:
    return ONT_TYPE