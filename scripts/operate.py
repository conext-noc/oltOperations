from helpers.handlers.smartolt import SmartOLT
from helpers.handlers.printer import log, inp


def onu_operate(*, smart_olt_client: SmartOLT, action: str, **kwargs):
    sn_count = int(inp(f"Ingrese el numero de ONTs a {'Activar' if 'enable' == action else 'Desactivar'}  :  "))
    sns = []
    for sn in range(sn_count):
        ont_sn = inp(f"Ingrese los ultimos 8 digitos del SN del Cliente {sn + 1}: ")
        sns.append(f"HWTC{ont_sn}")
    if len(sns) > 0:
        resp = smart_olt_client.operate_onu(onu_sns=sns, action=action)
        print(resp)
    else:
        log(value="No se ingreso ningun sn...",variant="warning")
    return
