from helpers.clientFinder.dataLookup import dataLookup
from helpers.utils.display import display
from helpers.utils.printer import colorFormatter, inp, log


def deleteClient(comm, command, quit, olt):
    lookupType = inp("Buscar cliente por serial o por Datos (F/S/P/ID) [S | D] : ")
    data = dataLookup(comm,command,olt,lookupType)
    if data["fail"] != None:
        log(colorFormatter(data["fail"], "fail"))
        quit()
        return
    proceed = display(data,"A")
    if not proceed:
        log(colorFormatter("Cancelando...", "warning"))
        quit()
        return
    for wan in data["wan"]:
        command(f"undo service-port {wan['spid']}")
        log(f"El SPID {wan['spid']} ha sido liberado!")
    command(f"interface gpon {data['frame']}/{data['slot']}")
    command(f"ont delete {data['port']} {data['id']}")
    log(colorFormatter(f"El cliente {data['name']} de {data['frame']}/{data['slot']}/{data['port']}/{data['id']} @ OLT {data['olt']} ha sido eliminado  ","success"))
    quit()
    return
    
