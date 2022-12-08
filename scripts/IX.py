import gspread
from helpers.addHandler import addONU, addOnuService
from helpers.clientDataLookup import lookup, newLookup
from helpers.printer import inp, log, colorFormatter
from helpers.opticalCheck import opticalValues
from helpers.spidHandler import availableSpid, verifySPID
from helpers.getWanData import preWan
from helpers.ontTypeHandler import typeCheck
from helpers.displayClient import display

providerMap = {"INTER": 1101, "VNET": 1102, "PUBLICAS": 1104, "VOIP": 101}

existing = {
    "CF": "Control flag            : ",
    "RE": "Run state               : ",
    "DESC": "Description             : ",
    "LDC": "Last down cause         : ",
}


def confirm(comm, command, olt, action, quit):
    sa = gspread.service_account(
        filename="service_account_olt_operations.json")
    sh = sa.open("CPDC")
    wks = sh.worksheet("DATOS")
    lstRow = len(wks.get_all_records()) + 2
    FRAME = None
    SLOT = None
    PORT = None
    NAME = None
    PROVIDER = None
    SN = None
    PLAN = None
    LP = None
    SRV = None
    SPID = None
    ID = None
    ONT_TYPE = None
    CI = None

    if action == "IN":
        (SN, FSP) = newLookup(comm, command, olt)
        keep = inp("Quiere continuar? [Y | N] : ").upper()
        if (keep == "Y"):
            FRAME = int(FSP.split("/")[0])
            SLOT = int(FSP.split("/")[1])
            PORT = int(FSP.split("/")[2])
            NAME = inp("Ingrese nombre del cliente : ").upper()[:56]
            CI = inp("Ingrese el NIF del cliente [V123 | J123]: ").upper()
            LP = inp(
                "Ingrese Line-Profile [PRUEBA_BRIDGE | INET | IP PUBLICAS | Bridging] : ")
            SRV = inp("Ingrese Service-Profile [Prueba | FTTH | Bridging] : ")

            SPID = availableSpid(comm, command)

            (ID, fail) = addONU(comm, command, FRAME,
                                SLOT, PORT, SN, NAME, SRV, LP)

            if fail != None:
                resp = colorFormatter(fail, "fail")
                log(resp)
                quit()
                return
        elif (keep == "N"):
            resp = colorFormatter(
                "SN no aparece en OLT, Saliendo...", "warning")
            log(resp)
            quit()
            return
        else:
            resp = colorFormatter(f"Opcion {keep} no existe", "fail")
            log(resp)
            quit()
            return

    elif action == "IP":
        lookupType = inp(
            "Buscar cliente por serial o por Datos de OLT [S | D] : ").upper()
        data = lookup(comm, command, olt, lookupType, False)
        if data["fail"] == None:
            if lookupType == "S" or lookupType == "D":
                proceed = display(data, "I")
                if proceed == "Y":
                    FRAME = data["frame"]
                    SLOT = data["slot"]
                    PORT = data["port"]
                    ID = data["id"]
                    SN = data["sn"]
                    NAME = data["name"]
                    SPID = availableSpid(comm, command)
                    CI = inp(
                        "Ingrese el NIF del cliente [V123 | J123]: ").upper()
                else:
                    resp = colorFormatter("Saliendo...", "warning")
                    log(resp)
                    quit()
                    return
        else:
            resp = colorFormatter(data["fail"], "fail")
            log(resp)
            quit()
            return

    if ID != None and ID != "F":
        resp = colorFormatter(
            f"El SPID que se le agregara al cliente es : {SPID}", "ok")
        log(resp)

        (temp, pwr) = opticalValues(comm, command, FRAME, SLOT, PORT, ID, True)

        proceed = inp(
            f"La potencia del ONT es : {pwr} y la temperatura es : {temp} \nquieres proceder con la instalacion? [Y | N] : "
        ).upper()

        if proceed == "Y":
            preg = inp(
                "Desea verificar si el cliente ya tiene la wan interface configurada? [Y | N] : ").upper()
            if preg == "Y":
                preWan(comm, command, SLOT, PORT, ID)
            Prov = inp(
                "Ingrese proevedor de cliente [INTER | VNET | PUBLICAS | VOIP] : ").upper()
            PLAN = inp("Ingrese plan de cliente : ").upper()
            PROVIDER = providerMap[Prov]
            ONT_TYPE = typeCheck(comm, command, FRAME, SLOT, PORT, ID)

            resp = colorFormatter(
                f"El tipo de ONT del cliente es {ONT_TYPE}", "ok")
            log(resp)

            addVlan = inp(
                "Se agregara vlan al puerto? [Y | N] : ").upper()

            if addVlan == "Y":
                command(f"interface gpon {FRAME}/{SLOT}")
                command(
                    f" ont  port  native-vlan  {PORT} {ID}  eth  1  vlan  {PROVIDER} ")
                command("quit")

            addOnuService(command, comm, SPID, PROVIDER,
                          FRAME, SLOT, PORT, ID, PLAN)

            verifySPID(comm, command, SPID)

            PLAN = PLAN[3:]

            template = """
    |{}  |  {}/{}/{}/{} 
    |OLT  {}  {}  {}
    |TEMPERATURA :   {}
    |POTENCIA    :   {}
    |SPID        :   {}""".format(
                NAME, FRAME, SLOT, PORT, ID, olt, Prov, PLAN, temp, pwr, SPID
            )
            res = colorFormatter(template, "success")
            wks.insert_row([SN, NAME, CI, olt, FRAME, SLOT, PORT,
                           ID, ONT_TYPE, "active", Prov, PLAN, SPID, "used"], lstRow)
            log(res)
            quit()
            return

        if proceed == "N":
            reason = inp("Por que no se le asignara servicio? : ").upper()
            template = """
    |{}  |  {}/{}/{}/{} 
    |OLT  {}  {}  {}
    |TEMPERATURA :   {}
    |POTENCIA    :   {}
    |SPID        :   {}
    |RAZÓN       :   {}""".format(
                NAME, FRAME, SLOT, PORT, ID, olt, PROVIDER, PLAN, temp, pwr, SPID, reason
            )
            res = colorFormatter(template, "success")
            log(res)
            quit()
            return
