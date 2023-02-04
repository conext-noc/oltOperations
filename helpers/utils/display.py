from helpers.utils.printer import colorFormatter, inp, log


def display(data, tp):
    """
    tp ==> type
    tp == A => all data will be displayed
    tp == I => data to installation concern will be displayed
    tp == B => only data will be displayed without input to be required
    """
    proceed = False
    if tp != "I":
        str1 = f"""
    |FRAME               :   {data["frame"]}
    |SLOT                :   {data["slot"]}
    |PORT                :   {data["port"]}
    |ID                  :   {data["onu_id"]}
    |NAME                :   {data["name"]}
    |SN                  :   {data["sn"]}
    |CONTROL FLAG        :   {data["control_flag"]}
    |RUN STATE           :   {data["run_state"]}
    |LAST DOWN CAUSE     :   {data["last_down_cause"]}
    |LAST DOWN TIME      :   {data["last_down_time"]}
    |LAST DOWN DATE      :   {data["last_down_date"]}
    |ONT TYPE            :   {data["device"]}
    |TEMPERATURA         :   {data["temp"]}
    |POTENCIA            :   {data["pwr"]}
    |IP                  :   {data["ip_address"]}
                """
        str2 = ""
        for idx, wanData in enumerate(data["wan"]):
            str2 += f"""
    |VLAN_{idx}              :   {wanData["vlan"]}
    |PLAN_{idx}              :   {wanData["plan_name"]}
    |SPID_{idx}              :   {wanData["spid"]}
    |STATE_{idx}             :   {wanData["state"]}
                """
        res = str1 + str2
        res = colorFormatter(str1, "ok") + colorFormatter(str2, "ok")
        log(res)
        val = inp("desea continuar? [Y|N] : ").upper() if tp == "A" else None
        proceed = True if val == "Y" and tp == "A" else False
    if tp == "I":
        str1 = f"""
    |FRAME               :   {data["frame"]}
    |SLOT                :   {data["slot"]}
    |PORT                :   {data["port"]}
    |ID                  :   {data["onu_id"]}
    |SN                  :   {data["sn"]}
    |ONT TYPE            :   {data["device"]}
    |NAME                :   {data["name"]}
    |CONTROL FLAG        :   {data["control_flag"]}
    |RUN STATE           :   {data["run_state"]}
                    """
        log(colorFormatter(str1, "ok"))
        val = inp("desea continuar? [Y|N] : ").upper()
        proceed = True if val == "Y" else False
    return proceed
