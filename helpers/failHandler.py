from helpers.outputDecoder import check, checkIter
from helpers.formatter import colorFormatter

failSTR = "Failure: "
endFail = "MARLLM0"


def failChecker(value):
    re = check(value, failSTR)
    if re == None:
        return None
    else:
        (_, s) = re.span()
        end = checkIter(value, endFail)
        maxLen = len(end) - 1
        (e, _) = end[maxLen]
        reason = value[s:e].replace("\n", "")
        reason = colorFormatter(reason, "fail")
        return reason
