import re

failSTR = "Failure: "


def failChecker(value):
    val = re.search(failSTR, value)
    if val == None:
        return None
    else:
        (_, e) = val.span()
        reason = value[e:]
        return reason
