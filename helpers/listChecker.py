from helpers.printer import log

def compare(odoo, drive, olt):
    listData = []
    for odooClient in odoo:
        for driveClient in drive:
            NIF1 = str(driveClient["NIF"])[1:]
            NIF2 = str(odooClient["Cliente/NIF"]).replace(".0","")
            if NIF2 == NIF1:
                if int(str(driveClient["OLT"]).replace(".0", "")) == int(olt):
                    FRAME = (
                        str(driveClient["FRAME"]).replace(".0", "")
                        if (
                            driveClient["FRAME"] != "N/A"
                            and driveClient["FRAME"] != ""
                            and driveClient["FRAME"] != "N/E"
                            and driveClient["FRAME"] != "N/A-E"
                            and driveClient["FRAME"] != "?"
                            and driveClient["FRAME"] != "S/I"
                            and driveClient["FRAME"] != "S/II"
                        )
                        else "NA"
                    )
                    SLOT = (
                        str(driveClient["SLOT"]).replace(".0", "")
                        if (
                            driveClient["SLOT"] != "N/A"
                            and driveClient["SLOT"] != ""
                            and driveClient["SLOT"] != "N/E"
                            and driveClient["SLOT"] != "N/A-E"
                            and driveClient["SLOT"] != "?"
                            and driveClient["SLOT"] != "S/I"
                            and driveClient["SLOT"] != "S/II"
                        )
                        else "NA"
                    )
                    PORT = (
                        str(driveClient["PORT"]).replace(".0", "")
                        if (
                            driveClient["PORT"] != "N/A"
                            and driveClient["PORT"] != ""
                            and driveClient["PORT"] != "N/E"
                            and driveClient["PORT"] != "N/A-E"
                            and driveClient["PORT"] != "?"
                            and driveClient["PORT"] != "S/I"
                            and driveClient["PORT"] != "S/II"
                        )
                        else "NA"
                    )
                    ID = (
                        str(driveClient["ID"]).replace(".0", "")
                        if (
                            driveClient["ID"] != "N/A"
                            and driveClient["ID"] != ""
                            and driveClient["ID"] != "N/E"
                            and driveClient["ID"] != "N/A-E"
                            and driveClient["ID"] != "?"
                            and driveClient["ID"] != "S/I"
                            and driveClient["ID"] != "S/II"
                        )
                        else "NA"
                    )
                    cliente = odooClient["Cliente"]
                    nombre = driveClient["NOMBRE"]
                    clienteNIF = odooClient["Cliente/NIF"]
                    idExterno = odooClient["ID externo"]
                    driveOLT = driveClient["OLT"]
                    log(f"{cliente} {nombre} {clienteNIF} {idExterno} {driveOLT} {FRAME} {SLOT} {PORT} {ID}")
                    listData.append(
                        {
                            "Cliente": odooClient["Cliente"],
                            "NOMBRE": driveClient["NOMBRE"],
                            "Cliente/NIF": odooClient["Cliente/NIF"],
                            "ID externo": odooClient["ID externo"],
                            "OLT": driveClient["OLT"],
                            "FRAME": FRAME,
                            "SLOT": SLOT,
                            "PORT": PORT,
                            "ID": ID,
                        }
                    )
    return listData
