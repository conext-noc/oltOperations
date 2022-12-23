from helpers.utils.printer import colorFormatter, log
from helpers.info.hashMaps import providerMap


def approved(data):
    template = f"""
    |{data['name']}  |  {data['frame']}/{data['slot']}/{data['port']}/{data['id']} 
    |OLT  {data['olt']}  {data["wan"][0]["vlan"]}  {data["wan"][0]["plan"]}
    |TEMPERATURA :   {data['temp']}
    |POTENCIA    :   {data['pwr']}
    |SPID        :   {data["wan"][0]["spid"]}"""
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
        data["wan"][0]['vlan'],
        data["wan"][0]["plan"],
        data["wan"][0]["spid"],
        "used",
        data["pwr"],
        data["temp"],
    ]


def denied(data, reason):
    template = f"""
    |{data['name']}  |  {data['frame']}/{data['slot']}/{data['port']}/{data['id']} 
    |OLT  {data['olt']}  {data["wan"][0]["vlan"]}  {data["wan"][0]["plan"]}
    |TEMPERATURA :   {data['temp']}
    |POTENCIA    :   {data['pwr']}
    |SPID        :   {data["wan"][0]['spid']}
    |RAZÓN       :   {reason}"""
    log(colorFormatter(template, "warning"))
