from helpers.printer import inp, log,colorFormatter
from helpers.clientDataLookup import lookup
import gspread
from helpers.displayClient import display

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
    lookupType = inp(
        "Buscar cliente por serial o por Datos de OLT [S | D] : ").upper()
    data = lookup(comm, command, OLT, lookupType)
    if data["fail"] == None:
        proceed = display(data,"A")
        if proceed == "Y":
            FRAME = data["FRAME"]
            SLOT = data["SLOT"]
            PORT = data["PORT"]
            ID = data["ID"]
            NAME = data["NAME"]
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
            log(resp)
            quit()
            return
    else:
        fail = colorFormatter(data["fail"], "fail")
        log(fail)
        quit()
        return
