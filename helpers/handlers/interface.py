from helpers.utils.decoder import check
from helpers.handlers.file_formatter import data_to_dict
from helpers.constants.regex_conditions import interface


def int_formatter(data, infc):
    (_, s) = check(data, interface["start"]).span()
    (e, _) = check(data, interface["end"]).span()
    value = data_to_dict(interface["header"], data[s:e])
    result = list(filter(lambda interface: interface["Interface"] == infc, value))[0]
    return result
