from helpers.handlers.printer import log, inp


def display(data, tp):
    """
    tp ==> type
    tp == A => all data will be displayed
    tp == B => only data will be displayed without input to be required
    """
    proceed = False
    res = f"""
|FRAME                      :   {data.get("frame", "*")}
|SLOT                       :   {data.get("slot", "*")}
|PORT                       :   {data.get("port", "*")}
|ONU_ID                     :   {data.get("onu_id", "*")}
|NAME                       :   {f'{data.get("name_1", "*")} {data.get("name_2", "*")} {data.get("contract", "*")}'}
|SN                         :   {data.get("sn", "*")}
|CONTROL FLAG               :   {data.get("state", "*")}
|RUN STATE                  :   {data.get("status", "*")}
|DIRECCION IP               :   {data.get("ip", "*")}
|MASCARA DE SUBRED          :   {data.get("mask", "*")}
|LAST DOWN CAUSE            :   {data.get("last_down_cause", "*")}
|LAST DOWN TIME             :   {data.get("last_down_time", "*")}
|LAST DOWN DATE             :   {data.get("last_down_date", "*")}
|ONT TYPE                   :   {data.get("device", "*")}
|TEMPERATURA                :   {data.get("temp", "*")}
|POTENCIA DE RECEPCION ONT  :   {data.get("pwr", "*")}
|POTENCIA DE RECEPCION OLT  :   {data.get("pwr_rx", "*")}
|VLAN                       :   {data.get("vlan", "*")}
|PLAN                       :   {data.get("plan_name", "*")}
|SPID                       :   {data.get("spid", "*")}
            """
    log(res, "ok")
    val = inp("desea continuar? [Y|N] : ").upper() if tp == "A" else None
    proceed = bool(val == "Y" and tp == "A")
    return proceed
