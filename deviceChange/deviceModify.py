def deviceModify(comm, command, enter, OLT):
    action = input(
        """
Que cambio se realizara? 
  > (CT)  :  Cambiar Titular
  > (CO)  :  Cambiar ONT
$ """
    )
    SLOT = input("Ingrese slot de cliente : ")
    PORT = input("Ingrese puerto de cliente : ")
    ID = input("Ingrese el id del cliente : ")
    enter()
    command(f"interface gpon 0/{SLOT}")
    if action == "CT":
        NAME = input("Ingrese nombre del cliente : ")
        command(f"ont modify {PORT} {ID} desc {NAME}")
        enter()
        print(
            f"Al Cliente 0/{SLOT}/{PORT}/{ID} OLT {OLT} se ha cambiado de titular a {NAME}"
        )
        return
    if action == "CO":
        SN = input("Ingrese el nuevo ont del cliente : ")
        command(f"ont modify {PORT} {ID} sn {SN}")
        enter()
        print(
            f"Al Cliente 0/{SLOT}/{PORT}/{ID} OLT {OLT} se ha sido cambiado el ont a {SN}"
        )
        return
