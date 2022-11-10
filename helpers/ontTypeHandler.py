from helpers.outputDecoder import check, decoder
from helpers.failHandler import failChecker

ontTypeStart = "OntProductDescription    : "
ontTypeEnd = "GPON Terminal"

def typeCheck(comm,command,FRAME,SLOT,PORT,ID):
  ONT_TYPE = None
  FAIL = None
  command(f"  interface  gpon  {FRAME}/{SLOT}  ")
  command(f"  display  ont  version  {PORT}  {ID}  ")
  command("quit")
  value = decoder(comm)
  FAIL = failChecker(value)
  if(FAIL == None):
    (_,tS) = check(value,ontTypeStart).span()
    (tE,_) = check(value, ontTypeEnd).span()
    ONT_TYPE = value[tS:tE]
    return (ONT_TYPE, FAIL)
  else:
    return(ONT_TYPE, FAIL)