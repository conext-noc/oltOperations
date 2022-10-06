def compare(odoo, drive, olt):
    listData = []
    for odooClient in odoo:
        for driveClient in drive:
            if(odooClient["Cliente/NIF"] == driveClient["NIF"][2:] ):
                if(driveClient["OLT"] == olt):
                    listData.append({
                        "Cliente": odooClient["Cliente"],
                        "NOMBRE": driveClient["NOMBRE"],
                        "Cliente/NIF": odooClient["Cliente/NIF"],
                        "ID externo": odooClient["ID externo"],
                        "OLT": driveClient["OLT"],
                        "FRAME": driveClient["FRAME"],
                        "SLOT": driveClient["SLOT"],
                        "PORT": driveClient["PORT"],
                        "ID": driveClient["ID"],
                        })
    return listData