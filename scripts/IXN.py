from time import sleep
from helpers.outputDecoder import decoder
from helpers.serviceMaper import plans, spidCalc
from helpers.displayClient import display
from helpers.ontTypeHandler import typeCheck
from helpers.spidHandler import verifySPID
from helpers.opticalCheck import opticalValues
from helpers.printer import inp, log, colorFormatter
from helpers.clientDataLookup import lookup, newLookup
from helpers.addHandler import addONU, addOnuServiceNew
from helpers.printer import colorFormatter
import gspread
import pygsheets
path = "./service_account_olt_operations.json"

existing = {
    "CF": "Control flag            : ",
    "RE": "Run state               : ",
    "DESC": "Description             : ",
    "LDC": "Last down cause         : ",
}


def confirmNew(comm, command, olt, action, quit):
    print("in new module olt")
    sa = gspread.service_account(
        filename="service_account_olt_operations.json")
    sh = sa.open("CPDC")
    wks = sh.worksheet("DATOS")
    lstRow = len(wks.get_all_records()) + 2
    data = {
        "frame": None,
        "slot": None,
        "port": None,
        "id": None,
        "name": None,
        "sn": None,
        "plan": None,
        "lineProfile": None,
        "srvProfile": None,
        "ontType": None,
        "nif": None,
        "fail": None,
        "gemPort": None,
        "vlan":None
    }

    if action == "IN":
        (data["sn"], FSP) = newLookup(comm, command, olt)
        proceed = inp("Quiere continuar? [Y | N] : ").upper()
        if (proceed == "Y"):
            data["frame"] = int(FSP.split("/")[0])
            data["slot"] = int(FSP.split("/")[1])
            data["port"] = int(FSP.split("/")[2])
            dataPlan = inp("Ingrese plan del cliente : ").upper()
            data["lineProfile"] = plans[dataPlan]["lineProfile"]
            data["srvProfile"] = plans[dataPlan]["srvProfile"]
            data["vlan"] = plans[dataPlan]["vlan"]
            data["plan"] = plans[dataPlan]["plan"]
            data["gemPort"] = plans[dataPlan]["gemPort"]
            data["name"] = inp("Ingrese nombre del cliente : ").upper()[:56]
            data["nif"] = inp(
                "Ingrese el NIF del cliente [V123 | J123]: ").upper()
            (data["id"], data["fail"]) = addONU(comm, command, data["frame"],
                                                data["slot"], data["port"], data["sn"], data["name"], data["srvProfile"], data["lineProfile"], olt)

            if data["fail"] != None:
                resp = colorFormatter(data["fail"], "fail")
                log(resp)
                quit()
                return
        elif (proceed == "N"):
            resp = colorFormatter(
                "SN no aparece en OLT, Saliendo...", "warning")
            log(resp)
            quit()
            return
        else:
            resp = colorFormatter(f"Opcion {proceed} no existe", "fail")
            log(resp)
            quit()
            return

    elif action == "IP":
        lookupType = inp(
            "Buscar cliente por serial o por Datos de OLT [S | D] : ").upper()
        data = lookup(comm, command, olt, lookupType, False)
        if data["fail"] == None:
            if lookupType != "S" or lookupType != "D":
                resp = colorFormatter(f"Opcion {proceed} no existe", "fail")
                log(resp)
                quit()
                return
            proceed = display(data, "I")
            if proceed == "Y":
                data["nif"] = inp(
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

    if data["id"] != None and data["id"] != "F":
        SPID = spidCalc(data["slot"], data["port"], data["id"])
        (temp, pwr) = opticalValues(comm, command, data["frame"],
                                    data["slot"], data["port"], data["id"], True)
        proceed = inp(
            f"La potencia del ONT es : {pwr} y la temperatura es : {temp} \nquieres proceder con la instalacion? [Y | N] : ").upper()

        if proceed == "Y":
            data["ontType"] = typeCheck(comm, command, data["frame"],
                                        data["slot"], data["port"], data["id"])
            resp = colorFormatter(
                "El tipo de ONT del cliente es {}".format(data["ontType"]), "ok")
            log(resp)
            command("interface gpon {}/{}".format(data["frame"],data["slot"]))
            command("ont ipconfig {} {} ip-index 2 dhcp vlan {}".format(
                data["port"], data["id"], data["vlan"]))
            command(
                "ont internet-config {} {} ip-index 2".format(data["port"], data["id"]))
            command(
                "ont policy-route-config {} {} profile-id 2".format(data["port"], data["id"]))
            addVlan = inp(
                "Se agregara vlan al puerto? [Y | N] : ").upper()
            if addVlan == "Y":
                command(
                    "interface gpon {}/{}".format(data["frame"], data["slot"]))
                command(
                    "ont port native-vlan {} {} eth 1 vlan {}".format(data["port"], data["id"], data["vlan"]))
            command("quit")
            out = decoder(comm)
            print(out)

            serviceType = inp("""
    > I : Internet
    > V : VoIP
    > P : Publicas
    $ """)

            addOnuServiceNew(command, comm, SPID[serviceType], data["vlan"], data["frame"],
                          data["slot"], data["port"], data["id"], data["plan"], data["gemPort"])
            verifySPID(comm, command, SPID[serviceType])
            
            sleep(15)
            
            command("interface gpon {}/{}".format(data["frame"], data["slot"]))
            command("ont wan-config {} {} ip-index 2 profile-id 0".format(data["port"], data["id"]))

            out = decoder(comm)
            print(out)
            template = """
    |{}  |  {}/{}/{}/{} 
    |OLT  {}  {}  {}
    |TEMPERATURA :   {}
    |POTENCIA    :   {}
    |SPID        :   {}""".format(
                data["name"], data["frame"],
                data["slot"], data["port"], data["id"], olt, data["vlan"], data["plan"], temp, pwr, SPID[serviceType]
            )
            res = colorFormatter(template, "success")
            wks.insert_row([data["sn"], data["name"], data["nif"], olt, data["frame"], data["slot"], data["port"],data["id"], data["ontType"], "active", data["vlan"], data["plan"], SPID[serviceType], "used"], lstRow)
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
                data["name"], data["frame"],
                data["slot"], data["port"], data["id"], olt, data["vlan"], data["plan"], temp, pwr, SPID[serviceType], reason
            )
            res = colorFormatter(template, "success")
            log(res)
            quit()
            return

        return