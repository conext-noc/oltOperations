from helpers.outputDecoder import check, checkIter
from helpers.formatter import colorFormatter

failSTR = "Failure: "
noExist = "The required ONT does not exist"

def failChecker(value):
    re = check(value,failSTR)
    reExist = check(value,noExist)
    reIter = checkIter(value,"MARLLM")
    if re == None and reExist == None:
        return None
    elif(reExist == None and re != None):
        (_, s) = re.span()
        (e,_) = reIter[2]
        reason = value[s:e].replace("\n", "")
        reason = colorFormatter(reason, "fail")
        return reason
    elif(reExist != None and re == None):
        reason = colorFormatter(noExist, "fail")
        return reason
