from helpers.constants.definitions import OnuLookup
from helpers.handlers.smartolt import SmartOLT
from helpers.handlers.printer import log, inp


def onu_update(*, smart_olt_client: SmartOLT, action: str, olt: int, **kwargs):
    if "serial" == action:
        sn_to_find = inp("Ingrese el SN del cliente  :  ")
        slot = int(inp("Ingrese la Tarjeta de OLT del cliente  :  "))
        port = int(inp("Ingrese el Puerto de OLT del cliente  :  "))
        client = smart_olt_client.get_client(is_bulk=False, lookup=OnuLookup(slot=slot, port=port, olt=olt, external_id=sn_to_find))
        
        if client is not None or len(client) > 0:
            log(value=client[0])
            new_sn = inp("Ingrese el nuevo SN del cliente  :  ")
            smart_olt_client.update_onu_sn(old_sn=sn_to_find, new_sn=new_sn)
            return