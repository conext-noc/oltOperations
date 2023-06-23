from helpers.utils.decoder import check, check_iter

END_FAIL = "MARLLM0"

FAILS = {
    "1": "Failure: ",
    "2": "% ",
    "3": "The required ONT does not exist",
    "4": "WAN port does not exist",
    "5": "The ONT does not exist",
    "6": "Port does not exist",
}


def fail_checker(value):
    reason = None
    fail = None
    for tries in list(FAILS.keys()):
        fail = check(value, FAILS[str(tries)])

    if fail is not None:
        (_, s) = fail.span()
        end = check_iter(value, END_FAIL)
        maxLen = len(end) - 1
        (e, _) = end[maxLen]
        reason = value[s:e].replace("\n", "")
        # log(FAILS[str(tries)], "fail")
    return reason
