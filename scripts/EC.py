from helpers.formatter import colorFormatter
from helpers.clientDataLookup import lookup
import gspread

existing = {
    "CF": "Control flag            : ",
    "RE": "Run state               : ",
    "DESC": "Description             : ",
    "LDC": "Last down cause         : ",
}


def delete(comm, command, OLT, quit):
    sa = gspread.service_account(
        filename="service_account_olt_operations.json")
    sh = sa.open("CPDC")
    wks = sh.worksheet("DATOS")
    FRAME = None
    SLOT = None
    PORT = None
    ID = None
    NAME = None
    STATE = None
    FAIL = None
    IPADDRESS = None
    TEMP = None
    PWR = None
    lookupType = input(
        "Buscar cliente por serial o por Datos de OLT [S | D] : ").upper()
    data = lookup(comm, command, OLT, lookupType)
    if data["fail"] == None:
        FRAME = data["frame"]
        SLOT = data["slot"]
        PORT = data["port"]
        ID = data["id"]
        NAME = data["name"]
        STATE = data["state"]
        IPADDRESS = data["ipAdd"]
        TEMP = data["temp"]
        PWR = data["pwr"]
        str1 = f"""
    FRAME               :   {FRAME}
    SLOT                :   {SLOT}
    PORT                :   {PORT}
    ID                  :   {ID}
    NAME                :   {NAME}
    SN                  :   {data["sn"]}
    ONT TYPE            :   {data["type"]}
    STATE               :   {STATE}
    STATUS              :   {data["status"]}
    LAST DOWN CAUSE     :   {data["ldc"]}
    IP                  :   {IPADDRESS}
    TEMPERATURA         :   {TEMP}
    POTENCIA            :   {PWR}
            """
        str2 = ""
        for idx, wanData in enumerate(data["wan"]):
            str2 += f"""
        VLAN_{idx}              :   {wanData["VLAN"]}
        PLAN_{idx}              :   {wanData["PLAN"]}
        SPID_{idx}              :   {wanData["SPID"]}
            """
        res = str1 + str2
        res = colorFormatter(res, "ok")
        print(res)
        proceed = input("Desea continuar? [Y | N]   :   ").upper()
        if proceed == "Y":
            for wanData in data["wan"]:
                spid = wanData["SPID"]
                command(f" undo  service-port  {spid}")
            command(f"interface gpon {FRAME}/{SLOT}")
            command(f"ont delete {PORT} {ID}")
            command("quit")
            resp = colorFormatter(
                f"{NAME} {FRAME}/{SLOT}/{PORT}/{ID} de OLT {OLT} ha sido eliminado", "ok")
            cell = wks.find(data["sn"])
            wks.delete_row(cell.row)
            print(resp)
            quit(3)
            return
    else:
        fail = colorFormatter(data["fail"], "fail")
        print(fail)
        quit(5)
        return
