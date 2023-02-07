from helpers.utils.printer import colorFormatter, log
from helpers.info.hashMaps import providerMap


def approved(data):
    template = f"""
    |{data['name']}  |  {data['frame']}/{data['slot']}/{data['port']}/{data['onu_id']} 
    |OLT  {data['olt']}  {data["wan"][0]["provider"]}  {data["plan_name"]}
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
        data["onu_id"],
        data["device"],
        "active",
        data["wan"][0]["provider"],
        data["plan_name"],
        data["wan"][0]["spid"],
        "used",
    ]
    
def denied(data, reason):
    template = f"""
    |{data['name']}  |  {data['frame']}/{data['slot']}/{data['port']}/{data['onu_id']} 
    |OLT  {data['olt']}  {data["wan"][0]["provider"]}  {data["plan_name"]}
    |TEMPERATURA :   {data['temp']}
    |POTENCIA    :   {data['pwr']}
    |RAZÓN       :   {reason}"""
    log(colorFormatter(template, "warning"))

def approvedDis(data):
    template = f"""
    |{data['name']}  |  {data['frame']}/{data['slot']}/{data['port']}/{data['onu_id']} 
    |OLT  {data['olt']}  {data["wan"][0]["provider"]}  {data["wan"][0]["plan_name"]}
    |TEMPERATURA :   {data['temp']}
    |POTENCIA    :   {data['pwr']}
    |SPID        :   {data["wan"][0]["spid"]}"""
    log(colorFormatter(template, "success"))