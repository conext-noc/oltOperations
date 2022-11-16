from helpers.outputDecoder import check, checkIter
from helpers.formatter import colorFormatter

failSTR = "Failure: "
failTp1 = "% "
endFail = "MARLLM0"
anotherFail = "The required ONT does not exist"
failAnother = "WAN port does not exist"


def failChecker(value):
    fail1 = check(value, failSTR)
    fail2 = check(value, failTp1)
    fail3 = check(value, anotherFail)
    fail4 = check(value, failAnother)
    if fail1 == None and fail2 == None and fail3 == None and fail4 == None:
        return None
    elif fail1 != None and fail2 == None and fail3 == None and fail4 == None:
        (_, s) = fail1.span()
        end = checkIter(value, endFail)
        maxLen = len(end) - 1
        (e, _) = end[maxLen]
        reason = value[s:e].replace("\n", "")
        reason = colorFormatter(reason, "fail")
        return reason
    elif fail1 == None and fail2 != None and fail3 == None and fail4 == None:
        (_, s) = fail2.span()
        end = checkIter(value, endFail)
        maxLen = len(end) - 1
        (e, _) = end[maxLen]
        reason = value[s:e].replace("\n", "")
        reason = colorFormatter(reason, "fail")
        return reason
    elif fail1 == None and fail2 == None and fail3 != None and fail4 == None:
        reason = colorFormatter(anotherFail, "fail")
        return reason
    elif fail1 == None and fail2 == None and fail3 == None and fail4 != None:
        reason = colorFormatter(failAnother, "fail")
        return reason
