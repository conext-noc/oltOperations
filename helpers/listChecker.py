def compare(odoo, drive, olt):
    listData = []
    for odooClient in odoo:
        for driveClient in drive:
            NIF1 = driveClient["NIF"][2:]
            NIF2 = odooClient["Cliente/NIF"]
            if int(NIF2) == int(NIF1):
                if int(driveClient["OLT"]) == int(olt):
                    FRAME = (
                        driveClient["FRAME"]
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
                        driveClient["SLOT"]
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
                        driveClient["PORT"]
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
                        driveClient["ID"]
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
                    print(
                        odooClient["Cliente"],
                        driveClient["NOMBRE"],
                        odooClient["Cliente/NIF"],
                        odooClient["ID externo"],
                        driveClient["OLT"],
                        FRAME,
                        SLOT,
                        PORT,
                        ID,
                    )
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
