import traceback
from time import sleep
from helpers.handlers.printer import inp, log
from helpers.constants.definitions import rtr_devices, olt_devices
from helpers.utils.ssh import ssh
from scripts.BC import client_lookup
from scripts.OX import client_operate
from scripts.XP import client_ports
from scripts.IC import client_install
from scripts.EC import client_delete
from scripts.MC import client_modify
from scripts.VC import client_traffic


def main():
    try:
        while True:
            action = inp(
                """
Que accion se realizara? 
    > (RL)  :   [OLT] Reactivar con lista
    > (RU)  :   [OLT] Reactivar uno
    > (SL)  :   [OLT] Suspender con lista
    > (SU)  :   [OLT] Suspender uno
    > (IC)  :   [OLT] Instalar Cliente
    > (BC)  :   [OLT] Buscar cliente en OLT
    > (EC)  :   [OLT] Eliminar Cliente
    > (MC)  :   [OLT] Modificar Cliente
    > (VC)  :   [OLT] Verificar consumo
    > (VP)  :   [OLT] Verificacion de puerto
    > (VT)  :   [OLT] Verificacion Total de Puertos en una OLT
    > (CA)  :   [OLT] Clientes con averias (corte de fibra)
    > (DT)  :   [OLT] Desactivados Totales
    > (MR)  :   [RTR] Monitorear Router
$ """
            )

            modules = {
                "RL": client_operate,
                "RU": client_operate,
                "SL": client_operate,
                "SU": client_operate,
                "IC": client_install,
                "BC": client_lookup,
                "EC": client_delete,
                "MC": client_modify,
                "VC": client_traffic,
                "VP": client_ports,
                "VT": client_ports,
                "CA": client_ports,
                "DT": client_ports,
                "MR": "interface_traffic",
            }

            MOD_KEYS = modules.keys()
            if action not in list(MOD_KEYS):
                log("Opcion No valida", "fail")
                sleep(2)
                return

            devices = olt_devices if action != "MR" else rtr_devices
            device = (
                inp("Seleccione la OLT a usar [1 | 2 | 3] : ")
                if action != "MR"
                else inp("Selecciona el router a monitorear [E1 | E2 | A1 | A2] : ")
            )
            debug = bool(
                inp("Enable debug [mostrar comandos]? (y/n): ").upper().strip() == "Y"
            )
            (comm, command, quit_ssh) = ssh(devices[device], debug)

            modules[action](comm, command, quit_ssh, device, action)

    except KeyboardInterrupt:
        log("Saliendo...", "warning")
        sleep(0.5)
    except Exception:
        log(f"Error At : {traceback.format_exc()}", "fail")
        sleep(10)


if __name__ == "__main__":
    main()
