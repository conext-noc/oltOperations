from helpers.handlers.printer import log


def approved(data):
    template = f"""
    |{data.get("name_1", "*")} {data.get("name_2", "*")} {data.get("contract", "*")}  |  {data.get('frame', "*")}/{data.get('slot', "*")}/{data.get('port', "*")}/{data.get('onu_id', "*")} 
    |OLT  {data.get('olt', "*")}  {data.get("wan", [{"provider":"*"}])[0]["provider"]}  {data.get("plan_name", "*")}
    |TEMPERATURA                  :   {data.get('temp', "*")}
    |POTENCIA DE RECEPCION ONT    :   {data.get('pwr', "*")}
    |POTENCIA De RECEPCION OLT    :   {data.get('pwr_tx', "*")}
    |SN                           :   {data.get('sn', "*")}
    |SPID                         :   {data.get("wan", [{"spid":"*"}])[0]["spid"]}"""
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
        data.get("wan",[{"provider":"*"}])[0]["provider"],
        data.get("plan_name"),
        data.get("wan", [{"spid":"*"}])[0]["spid"],
        "used",
    ]


def denied(data, reason):
    template = f"""
    {data.get("name_1", "*")} {data.get("name_2", "*")} {data.get("contract", "*")}  |  {data.get('frame', "*")}/{data.get('slot', "*")}/{data.get('port', "*")}/{data.get('onu_id', "*")}
    |OLT  {data.get('olt', "*")}  {data.get("provider", "*")} {data.get("plan_name", "*")}
    |TEMPERATURA                  :   {data.get('temp', "*")}
    |POTENCIA DE RECEPCION ONT    :   {data.get('pwr', "*")}
    |POTENCIA De RECEPCION OLT    :   {data.get('pwr_tx', "*")}
    |SN                           :   {data.get('sn', "*")}
    |RAZÓN                        :   {reason}"""
    log(template, "warning")


def approvedDis(data):
    template = f"""
    |{f'{data.get("name_1", "*")} {data.get("name_2", "*")} {data.get("contract", "*")}'} 
    |{data.get('frame', "*")}/{data.get('slot', "*")}/{data.get('port', "*")}/{data.get('onu_id', "*")} 
    |OLT  {data.get('olt', "*")}  {data.get("provider", "*")}  {data.get("plan_name", "*")}
    |TEMPERATURA                  :   {data.get('temp', "*")}
    |POTENCIA DE RECEPCION ONT    :   {data.get('pwr', "*")}
    |POTENCIA De RECEPCION OLT    :   {data.get('pwr_tx', "*")}
    |SN                           :   {data.get('sn', "*")}
    |SPID                         :   {data.get("spid", "*")}"""
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
        f'{data.get("name_1", "*")} {data.get("name_2", "*")} {data.get("contract", "*")}',
        data.get("frame", "*"),
        data.get("slot", "*"),
        data.get("port", "*"),
        data.get("onu_id", "*"),
        types[changeType],
        newVal,
    )
    return msg
