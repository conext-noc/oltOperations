from tkinter import filedialog
from helpers.csvParser import parser
from helpers.listChecker import compare

def deactivate(comm,enter,command,olt):
    actionList = []
    typeOfList = input("Se requieren datos de odoo? [Y/N] : ")
    accion = ""
    if(typeOfList == "Y"):
        accion = "CO"
        print("Selecciona el archivo de lista de clientes de ODOO")
        odoo = filedialog.askopenfilename()
        print("Selecciona el archivo de lista de clientes de Drive")
        drive = filedialog.askopenfilename()
        actionList = compare(parser(odoo),parser(drive), olt)

    elif(typeOfList == "N"):
        accion = "CC"
        print("Selecciona la lista de clientes")
        lista = filedialog.askopenfilename()
        actionList = parser(lista)
    else:
        raise Exception("""Ningun tipo de lista se ha seleccionado, tip: respuestas posibles "Y" para listas con datos de ODOO y "N" para listas sin datos de ODOO""")
    if(len(actionList) > 0):
        for client in actionList:
            print(client)
            command(
                "interface gpon {}/{}".format(client["FRAME"], client["SLOT"]))
            enter()
            command("ont deactivate {} {}".format(
                client["PORT"], client["ID"]))
            enter()
            command("display ont info {} {} | include \"Control flag\" ".format(
                client["PORT"], client["ID"]))
            enter()
            command("quit")
            enter()
            outputClient = comm.recv(65535)
            outputClient = outputClient.decode("ascii")
            OLT = client["OLT"]
            FRAME = client["FRAME"]
            SLOT = client["SLOT"]
            PORT = client["PORT"]
            clientID = client["ID"]
            path = f"{accion}_{FRAME}-{SLOT}-{PORT}-{clientID}_OLT{OLT}.txt"
            print(outputClient, file=open(path, "w"))
        return actionList
    else:
        raise Exception("la lista no tiene ningun cliente...")
