import gspread
from helpers.addHandler import addONU, addOnuService
from helpers.clientDataLookup import lookup
from helpers.formatter import colorFormatter
from helpers.opticalCheck import opticalValues
from helpers.spidHandler import availableSpid, verifySPID
from helpers.getWanData import preWan
from helpers.ontTypeHandler import typeCheck

providerMap = {"INTER": 1101, "VNET": 1102, "PUBLICAS": 1104}

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
    if action == "IN":
        FRAME = input("Ingrese frame de cliente : ").upper()
        SLOT = input("Ingrese slot de cliente : ").upper()
        PORT = input("Ingrese puerto de cliente : ").upper()
        NAME = input("Ingrese nombre del cliente : ").upper()
        SN = input("Ingrese serial de cliente : ").upper()
        PLAN = input("Ingrese plan de cliente : ").upper()
        LP = input(
            "Ingrese Line-Profile [PRUEBA_BRIDGE | INET | IP PUBLICAS | Bridging] : ")
        SRV = input("Ingrese Service-Profile [Prueba | FTTH | Bridging] : ")

        SPID = availableSpid(comm, command)

        (ID, fail) = addONU(comm, command, FRAME, SLOT, PORT, SN, NAME, SRV, LP)

        if fail != None:
            resp = colorFormatter(fail, "fail")
            print(resp)
            quit(5)
            return

    elif action == "IP":
        lookupType = input(
            "Buscar cliente por serial o por Datos de OLT [S | D] : ").upper()
        data = lookup(comm, command, olt, lookupType, False)
        if data["fail"] == None:
            if lookupType == "S" or lookupType == "D":
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
                print(colorFormatter(str1, "ok"))
            FRAME = data["frame"]
            SLOT = data["slot"]
            PORT = data["port"]
            ID = data["id"]
            NAME = data["name"]
            PROVIDER = input(
                "Ingrese proevedor de cliente [INTER | VNET | PUBLICAS] : ").upper()
            PLAN = input("Ingrese plan de cliente : ").upper()
            SPID = availableSpid(comm, command)
        else:
            resp = colorFormatter(data["fail"], "fail")
            print(resp)
            quit(5)
            return

    if ID != None and ID != "F":
        resp = colorFormatter(
            f"El SPID que se le agregara al cliente es : {SPID}", "ok")
        print(resp)

        (temp, pwr) = opticalValues(comm, command, FRAME, SLOT, PORT, ID, True)

        proceed = input(
            f"La potencia del ONT es : {pwr} y la temperatura es : {temp} \nquieres proceder con la instalacion? [Y | N] : "
        ).upper()

        if proceed == "Y":
            preg = input(
                "Desea verificar si el cliente ya tiene la wan interface configurada? [Y | N] : ").upper()
            if preg == "Y":
                preWan(comm, command, SLOT, PORT, ID)
            Prov = input(
                "Ingrese proevedor de cliente [INTER | VNET | PUBLICAS] : ").upper()

            PROVIDER = providerMap[Prov]
            ONT_TYPE = typeCheck(comm, command, FRAME, SLOT, PORT, ID)

            resp = colorFormatter(
                f"El tipo de ONT del cliente es {ONT_TYPE}", "ok")
            print(resp)

            addVlan = input(
                "Se agregara vlan al puerto? [Y | N] : ").upper()

            if addVlan == "Y":
                command(f"interface gpon {FRAME}/{SLOT}")
                command(
                    f" ont  port  native-vlan  {PORT} {ID}  eth  1  vlan  {PROVIDER} ")
                command("quit")

            addOnuService(command, comm, SPID,PROVIDER, FRAME, SLOT, PORT, ID, PLAN)
            
            verifySPID(comm, command, SPID)
            
            PLAN = PLAN[3:]
            
            template = """
    |{}  |  {}/{}/{}/{} 
    |OLT  {}  {}  {}
    |TEMPERATURA :   {}
    |POTENCIA    :   {}
    |SPID        :   {}""".format(
                NAME, FRAME, SLOT, PORT, ID, olt, PROVIDER, PLAN, temp, pwr, SPID
            )
            res = colorFormatter(template, "success")
            wks.insert_row([SN, NAME, olt, FRAME, SLOT, PORT,
                           ID, ONT_TYPE, PROVIDER, PLAN, SPID], lstRow)
            print(res)
            quit(10)
            return
        
        if proceed == "N":
            reason = input("Por que no se le asignara servicio? : ").upper()
            PLAN = PLAN[3:]
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
            print(res)
            quit(5)
            return
