from helpers.handlers.printer import log, inp


def display(data, tp):
    """
    tp ==> type
    tp == A => all data will be displayed
    tp == B => only data will be displayed without input to be required
    """
    proceed = False
    res = f"""
|FRAME                      :   {data["frame"]}
|SLOT                       :   {data["slot"]}
|PORT                       :   {data["port"]}
|ONU_ID                     :   {data["onu_id"]}
|NAME                       :   {f'{data["name_1"]} {data["name_2"]} {data["contract"]}'}
|SN                         :   {data["sn"]}
|CONTROL FLAG               :   {data["state"]}
|RUN STATE                  :   {data["status"]}
|DIRECCION IP               :   {data["ip"]}
|MASCARA DE SUBRED          :   {data["mask"]}
|LAST DOWN CAUSE            :   {data.get("last_down_cause") or "N/A"}
|LAST DOWN TIME             :   {data.get("last_down_time") or "N/A"}
|LAST DOWN DATE             :   {data.get("last_down_date") or "N/A"}
|ONT TYPE                   :   {data["device"]}
|TEMPERATURA                :   {data["temp"]}
|POTENCIA DE RECEPCION ONT  :   {data["pwr"]}
|POTENCIA DE RECEPCION OLT  :   {data["pwr_rx"]}
|VLAN                       :   {data["vlan"]}
|PLAN                       :   {data["plan_name"]}
|SPID                       :   {data["spid"]}
            """
    log(res, "ok")
    val = inp("desea continuar? [Y|N] : ").upper() if tp == "A" else None
    proceed = bool(val == "Y" and tp == "A")
    return proceed
