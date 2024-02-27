from helpers.handlers.printer import log, inp


def display(data, tp):
    """
    tp ==> type
    tp == A => all data will be displayed
    tp == B => only data will be displayed without input to be required
    """
    proceed = False
    res = f"""
|FRAME                      :   {data.get("frame", "N/A")}
|SLOT                       :   {data.get("slot", "N/A")}
|PORT                       :   {data.get("port", "N/A")}
|ONU_ID                     :   {data.get("onu_id", "N/A")}
|NAME                       :   {f'{data.get("name_1", "N/A")} {data.get("name_2", "N/A")} {data.get("contract", "N/A")}'}
|SN                         :   {data.get("sn", "N/A")}
|CONTROL FLAG               :   {data.get("state", "N/A")}
|RUN STATE                  :   {data.get("status", "N/A")}
|DIRECCION IP               :   {data.get("ip", "N/A")}
|MASCARA DE SUBRED          :   {data.get("mask", "N/A")}
|LAST DOWN CAUSE            :   {data.get("last_down_cause", "N/A")}
|LAST DOWN TIME             :   {data.get("last_down_time", "N/A")}
|LAST DOWN DATE             :   {data.get("last_down_date", "N/A")}
|ONT TYPE                   :   {data.get("device", "N/A")}
|TEMPERATURA                :   {data.get("temp", "N/A")}
|POTENCIA DE RECEPCION ONT  :   {data.get("pwr", "N/A")}
|POTENCIA DE RECEPCION OLT  :   {data.get("pwr_rx", "N/A")}
|VLAN                       :   {data.get("vlan", "N/A")}
|PLAN                       :   {data.get("plan_name", "N/A")}
|SPID                       :   {data.get("spid", "N/A")}
            """
    log(res, "ok")
    val = inp("desea continuar? [Y|N] : ").upper() if tp == "A" else None
    proceed = bool(val == "Y" and tp == "A")
    return proceed
