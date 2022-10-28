from helpers.serialLookup import serialSearch

def deviceModify(comm, command, OLT):
    FRAME = ""
    SLOT = ""
    PORT = ""
    ID = ""
    action = input(
        """
Que cambio se realizara? 
  > (CT)  :  Cambiar Titular
  > (CO)  :  Cambiar ONT
$ """
    )
    lookupType = input("Buscar cliente por serial o por F/S/P [S | F] : ")
    if(lookupType == "S"):
        SN = input("Ingrese el Serial del Cliente a buscar : ")
        (FRAME,SLOT,PORT,ID,NAME,STATE) = serialSearch(comm,command,SN)
    if(lookupType == "F"):
        FRAME = input("Ingrese frame de cliente : ")
        SLOT = input("Ingrese slot de cliente : ")
        PORT = input("Ingrese puerto de cliente : ")
        ID = input("Ingrese el id del cliente : ")
    command(f"interface gpon {FRAME}/{SLOT}")
    if action == "CT":
        NAME = input("Ingrese el nuevo nombre del cliente : ")
        command(f"ont modify {PORT} {ID} desc {NAME}")
        print(
            f"Al Cliente {FRAME}/{SLOT}/{PORT}/{ID} OLT {OLT} se ha cambiado de titular a {NAME}"
        )
        return
    if action == "CO":
        SN = input("Ingrese el nuevo ont del cliente : ")
        command(f"ont modify {PORT} {ID} sn {SN}")
        print(
            f"Al Cliente 0/{SLOT}/{PORT}/{ID} OLT {OLT} se ha sido cambiado el ont a {SN}"
        )
        return
