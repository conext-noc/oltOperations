from helpers.utils.printer import colorFormatter, log
from helpers.info.hashMaps import providerMap


def approved(data):
    template = f"""
    |{data['name']}  |  {data['frame']}/{data['slot']}/{data['port']}/{data['id']} 
    |OLT  {data['olt']}  {data["vlan"]}  {data['plan']}
    |TEMPERATURA :   {data['temp']}
    |POTENCIA    :   {data['pwr']}
    |SPID        :   {data['spid']}"""
    log(colorFormatter(template, "success"))
    return [
        data["sn"],
        data["name"],
        data["nif"],
        data["olt"],
        data["frame"],
        data["slot"],
        data["port"],
        data["id"],
        data["device"],
        "active",
        data['vlan'],
        data["plan"],
        data["spid"],
        "used",
    ]


def denied(data, reason):
    template = f"""
    |{data['name']}  |  {data['frame']}/{data['slot']}/{data['port']}/{data['id']} 
    |OLT  {data['olt']}  NA  NA
    |TEMPERATURA :   {data['temp']}
    |POTENCIA    :   {data['pwr']}
    |SPID        :   {data['spid']}
    |RAZÓN       :   {reason}"""
    log(colorFormatter(template, "warning"))
