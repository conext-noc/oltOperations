from helpers.constants.definitions import OnuLookup
from helpers.handlers.smartolt import SmartOLT
from helpers.handlers.printer import log, inp


def onu_display(*, smart_olt_client: SmartOLT, action: str, olt: int, **kwargs):
    if "table" == action:
        slot = int(inp("Ingrese la Tarjeta de OLT del los clientes  :  "))
        port = int(inp("Ingrese el Puerto de OLT del los clientes  :  "))
        clients = smart_olt_client.get_client(is_bulk=True, lookup=OnuLookup(slot=slot, port=port, olt=olt))
        for client in clients:
            log(value=client)
        return
    if "single" == action:
        sn_to_find = inp("Ingrese el SN del cliente  :  ")
        slot = int(inp("Ingrese la Tarjeta de OLT del cliente  :  "))
        port = int(inp("Ingrese el Puerto de OLT del cliente  :  "))
        client = smart_olt_client.get_client(is_bulk=False, lookup=OnuLookup(slot=slot, port=port, olt=olt, external_id=sn_to_find))
        log(value=client[0])
        return
