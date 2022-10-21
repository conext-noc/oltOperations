from helpers.ontCheck import verifyValues

def valueVerify(comm, command, enter):
    SLOT = input("Ingrese slot de cliente : ")
    PORT = input("Ingrese puerto de cliente : ")
    ID = input("Ingrese el id del cliente : ")
    (TEMP, PWR) = verifyValues(comm, command, enter, SLOT, PORT, ID)
    print(f"""
La potencia del ONT es : {PWR}
La temperatura es : {TEMP}
"""
    )
