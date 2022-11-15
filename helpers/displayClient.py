from helpers.formatter import colorFormatter

def display(data,ALL=True,i=False):
  if ALL:
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
    |IP                  :   {data["ipAdd"]}
    |TEMPERATURA         :   {data["temp"]}
    |POTENCIA            :   {data["pwr"]}
                """
    str2 = ""
    for idx, wanData in enumerate(data["wan"]):
                str2 += f"""
    |VLAN_{idx}              :   {wanData["VLAN"]}
    |PLAN_{idx}              :   {wanData["PLAN"]}
    |SPID_{idx}              :   {wanData["SPID"]}
                """
    res = str1 + str2
    res = colorFormatter(res, "ok")
    print(res)
  proceed = input("desea continuar? [Y|N] : ").upper()
  return proceed