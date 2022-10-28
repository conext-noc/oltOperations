from helpers.outputDecoder import check, checkIter

failSTR = "Failure: "

def failChecker(value):
    re = check(value,failSTR)
    if re == None:
        return None
    else:
        (_, s) = re.span()
        reason = value[s:s+25].replace("\n", "")
        return reason
