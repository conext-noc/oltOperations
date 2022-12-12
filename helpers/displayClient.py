from helpers.printer import colorFormatter, inp, log


def display(data, tp):
    """
    tp ==> type
    tp == A => all data will be displayed
    tp == I => data to installation concern will be displayed
    tp == B => only data will be displayed without input to be required
    """
    proceed = None
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
    |ONT TYPE            :   {data["type"]}
    |TEMPERATURA         :   {data["temp"]}
    |POTENCIA            :   {data["pwr"]}
    |IP                  :   {data["ipAdd"]}
                """
        str2 = ""
        for idx, wanData in enumerate(data["wan"]):
            str2 += f"""
    |VLAN_{idx}              :   {wanData["VLAN"]}
    |PLAN_{idx}              :   {wanData["PLAN"]}
    |SPID_{idx}              :   {wanData["SPID"]}
                """
        res = str1 + str2
        res = colorFormatter(str1, "ok") + colorFormatter(str2, "ok")
        log(res)
        proceed = inp("desea continuar? [Y|N] : ").upper()
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
    |ONT TYPE            :   {data["type"]}
    |TEMPERATURA         :   {data["temp"]}
    |POTENCIA            :   {data["pwr"]}
    |IP                  :   {data["ipAdd"]}
                """
        str2 = ""
        for idx, wanData in enumerate(data["wan"]):
            str2 += f"""
    |VLAN_{idx}              :   {wanData["VLAN"]}
    |PLAN_{idx}              :   {wanData["PLAN"]}
    |SPID_{idx}              :   {wanData["SPID"]}
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
    ONT TYPE            :   {data["type"]}
    NAME                :   {data["name"]}
    STATE               :   {data["state"]}
    STATUS              :   {data["status"]}
                    """
        log(colorFormatter(str1, "ok"))
        proceed = inp("desea continuar? [Y|N] : ").upper()
    return proceed
