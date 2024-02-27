from helpers.handlers.printer import log


def approved(data):
    template = f"""
    |{data.get("name_1", "N/A")} {data.get("name_2", "N/A")} {data.get("contract", "N/A")}  |  {data.get('frame', "N/A")}/{data.get('slot', "N/A")}/{data.get('port', "N/A")}/{data.get('onu_id', "N/A")} 
    |OLT  {data.get('olt', "N/A")}  {data.get("wan", [{"provider":"N/A"}])[0]["provider"]}  {data.get("plan_name", "N/A")}
    |TEMPERATURA :   {data.get('temp', "N/A")}
    |POTENCIA    :   {data.get('pwr', "N/A")}
    |SN          :   {data.get('sn', "N/A")}
    |SPID        :   {data.get("wan", [{"spid":"N/A"}])[0]["spid"]}"""
    log(template, "success")
    return [
        data.get("sn"),
        f'{data.get("name_1")} {data.get("name_2")} {data.get("contract")}',
        data.get("olt"),
        data.get("frame"),
        data.get("slot"),
        data.get("port"),
        data.get("onu_id"),
        data.get("device"),
        "active",
        data.get("wan",[{"provider":"N/A"}])[0]["provider"],
        data.get("plan_name"),
        data.get("wan", [{"spid":"N/A"}])[0]["spid"],
        "used",
    ]


def denied(data, reason):
    template = f"""
    {data.get("name_1", "N/A")} {data.get("name_2", "N/A")} {data.get("contract", "N/A")}  |  {data.get('frame', "N/A")}/{data.get('slot', "N/A")}/{data.get('port', "N/A")}/{data.get('onu_id', "N/A")}
    |OLT  {data.get('olt', "N/A")}  {data.get("provider", "N/A")} {data.get("plan_name", "N/A")}
    |TEMPERATURA :   {data.get('temp', "N/A")}
    |POTENCIA    :   {data.get('pwr', "N/A")}
    |SN          :   {data.get('sn', "N/A")}
    |RAZÓN       :   {reason}"""
    log(template, "warning")


def approvedDis(data):
    template = f"""
    |{f'{data.get("name_1", "N/A")} {data.get("name_2", "N/A")} {data.get("contract", "N/A")}'} 
    |{data.get('frame', "N/A")}/{data.get('slot', "N/A")}/{data.get('port', "N/A")}/{data.get('onu_id', "N/A")} 
    |OLT  {data.get('olt', "N/A")}  {data.get("provider", "N/A")}  {data.get("plan_name", "N/A")}
    |TEMPERATURA :   {data.get('temp', "N/A")}
    |POTENCIA    :   {data.get('pwr', "N/A")}
    |SN          :   {data.get('sn', "N/A")}
    |SPID        :   {data.get("spid", "N/A")}"""
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
        f'{data.get("name_1", "N/A")} {data.get("name_2", "N/A")} {data.get("contract", "N/A")}',
        data.get("frame", "N/A"),
        data.get("slot", "N/A"),
        data.get("port", "N/A"),
        data.get("onu_id", "N/A"),
        types[changeType],
        newVal,
    )
    return msg
