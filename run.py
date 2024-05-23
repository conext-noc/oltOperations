import traceback
from time import sleep
from helpers.handlers.smartolt import SmartOLT
from helpers.handlers.printer import log, inp
from scripts.display import onu_display
from scripts.install import onu_install
from scripts.operate import onu_operate
from scripts.update import onu_update


def main():
    try:
        while True:
            smart_olt = SmartOLT()
            action = inp(
                """
Que accion se realizara? 
    > ( 1)  :   [OLT] Reactivar ONT(s)
    > ( 2)  :   [OLT] Suspender ONT(s)
    > ( 3)  :   [OLT] Instalar Cliente
    > ( 4)  :   [OLT] Buscar cliente en OLT
    > ( 5)  :   [OLT] Modificar Cliente
    > ( 6)  :   [OLT] Verificacion de puerto
$ """
            )

            modules = {
                "1": (onu_operate, "enable"),
                "2": (onu_operate, "disable"),
                "3": (onu_install, "install"),
                "4": (onu_display, "single"),
                "5": (onu_update, "serial"),
                "6": (onu_display, "table"),
            }

            MOD_KEYS = modules.keys()
            if action not in list(MOD_KEYS):
                log(value="Opcion No valida", variant="fail")
                sleep(2)
                return
            device = inp("Seleccione la OLT a usar [1 | 2] : ")
            olt = 5 if "1" == device else 4
            modules[action][0](
                smart_olt_client=smart_olt, action=modules[action][1], olt=olt
            )

    except KeyboardInterrupt:
        log(value="Saliendo...", variant="warning")
        sleep(0.5)
    except Exception as e:
        log(
            value=f"Error At : {traceback.format_exc()} || {e.__traceback__.tb_lineno}",
            variant="fail",
        )
        sleep(10)


if __name__ == "__main__":
    main()
