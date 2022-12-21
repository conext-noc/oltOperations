from helpers.utils.printer import colorFormatter, inp, log


def display(data, tp):
    """
    tp ==> type
    tp == A => all data will be displayed
    tp == I => data to installation concern will be displayed
    tp == B => only data will be displayed without input to be required
    """
    proceed = False
    if tp == "A":
        str1 = f"""
    |FRAME               :   {data["frame"]}
    |SLOT                :   {data["slot"]}
    |PORT                :   {data["port"]}
    |ID                  :   {data["id"]}
    |NAME                :   {data["name"]}
    |SN                  :   {data["sn"]}
    |STATE               :   {data["state"]}
    |STATUS              :   {data["status"]}
    |LAST DOWN CAUSE     :   {data["ldc"]}
    |ONT TYPE            :   {data["device"]}
    |TEMPERATURA         :   {data["temp"]}
    |POTENCIA            :   {data["pwr"]}
    |IP                  :   {data["ipAdd"]}
                """
        str2 = ""
        for idx, wanData in enumerate(data["wan"]):
            str2 += f"""
    |VLAN_{idx}              :   {wanData["vlan"]}
    |PLAN_{idx}              :   {wanData["plan"]}
    |SPID_{idx}              :   {wanData["spid"]}
                """
        res = str1 + str2
        res = colorFormatter(str1, "ok") + colorFormatter(str2, "ok")
        log(res)
        val = inp("desea continuar? [Y|N] : ").upper()
        proceed = True if val == "Y" else False
    if tp == "B":
        str1 = f"""
    |FRAME               :   {data["frame"]}
    |SLOT                :   {data["slot"]}
    |PORT                :   {data["port"]}
    |ID                  :   {data["id"]}
    |NAME                :   {data["name"]}
    |SN                  :   {data["sn"]}
    |STATE               :   {data["state"]}
    |STATUS              :   {data["status"]}
    |LAST DOWN CAUSE     :   {data["ldc"]}
    |ONT TYPE            :   {data["device"]}
    |TEMPERATURA         :   {data["temp"]}
    |POTENCIA            :   {data["pwr"]}
    |IP                  :   {data["ipAdd"]}
                """
        str2 = ""
        for idx, wanData in enumerate(data["wan"]):
            str2 += f"""
    |VLAN_{idx}              :   {wanData["vlan"]}
    |PLAN_{idx}              :   {wanData["plan"]}
    |SPID_{idx}              :   {wanData["spid"]}
                """
        res = str1 + str2
        res = colorFormatter(str1, "ok") + colorFormatter(str2, "ok")
        log(res)
    if tp == "I":
        str1 = f"""
    FRAME               :   {data["frame"]}
    SLOT                :   {data["slot"]}
    PORT                :   {data["port"]}
    ID                  :   {data["id"]}
    SN                  :   {data["sn"]}
    ONT TYPE            :   {data["device"]}
    NAME                :   {data["name"]}
    STATE               :   {data["state"]}
    STATUS              :   {data["status"]}
                    """
        log(colorFormatter(str1, "ok"))
        val = inp("desea continuar? [Y|N] : ").upper()
        proceed = True if val == "Y" else False
    return proceed
