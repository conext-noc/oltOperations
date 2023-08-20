from helpers.handlers.printer import log


def approved(data):
    template = f"""
    |{data["name_1"]} {data["name_2"]} {data["contract"]}  |  {data['frame']}/{data['slot']}/{data['port']}/{data['onu_id']} 
    |OLT  {data['olt']}  {data["wan"][0]["provider"]}  {data["plan_name"]}
    |TEMPERATURA :   {data['temp']}
    |POTENCIA    :   {data['pwr']}
    |SN          :   {data['sn']}
    |SPID        :   {data["wan"][0]["spid"]}"""
    log(template, "success")
    return [
        data["sn"],
        f'{data["name_1"]} {data["name_2"]} {data["contract"]}',
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
    |OLT  {data['olt']}  {data["provider"]}  {data["plan_name"]}
    |TEMPERATURA :   {data['temp']}
    |POTENCIA    :   {data['pwr']}
    |SN          :   {data['sn']}
    |RAZÓN       :   {reason}"""
    log(template, "warning")


def approvedDis(data):
    template = f"""
    |{f'{data["name_1"]} {data["name_2"]} {data["contract"]}'} 
    |{data['frame']}/{data['slot']}/{data['port']}/{data['onu_id']} 
    |OLT  {data['olt']}  {data["provider"]}  {data["plan_name"]}
    |TEMPERATURA :   {data['temp']}
    |POTENCIA    :   {data['pwr']}
    |SN          :   {data['sn']}
    |SPID        :   {data["spid"]}"""
    log(template, "success")


def change(data, changeType, newVal):
    types = {
        "CP": "cambiado el Plan a",
        "CT": "cambiado el Nombre a",
        "CO": "cambiado el ONT a",
        "CV": "cambiado el Proveedor a",
        "ES": "Elimiado el SPID",
        "AS": "Agregado el plan y vlan a",
    }
    msg = """
    |Al cliente {}
    |{}/{}/{}/{}
    |se le ha {} '{}'
    """.format(
        f'{data["name_1"]} {data["name_2"]} {data["contract"]}',
        data["frame"],
        data["slot"],
        data["port"],
        data["onu_id"],
        types[changeType],
        newVal,
    )
    return msg
