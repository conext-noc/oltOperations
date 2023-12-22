import traceback
from time import sleep
from helpers.constants.definitions import rtr_devices, olt_devices
from helpers.utils.ssh import ssh
from scripts.ACL import device_acl
from scripts.BC import client_lookup
from scripts.MP import data_plan_migration
from scripts.OX import client_operate
from scripts.XP import client_ports
from scripts.IC import client_install
from scripts.EC import client_delete
from scripts.MC import client_modify
from scripts.VC import client_traffic
from scripts.MR import router_monitor
from scripts.SYNC_DB import db_sync
from helpers.handlers.printer import inp, log

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
    > (DB)  :   [OLT] Sincronizar estatus de corte db-olt
    > (MP)  :   [OLT] Migrar Planes
    > (MR)  :   [RTR] Monitorear Router
    > (OA)  :   [OLT] validar/actualizar acl lists en OLT
    > (RA)  :   [RTR] validar/actualizar acl lists en RTR
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
                "MR": router_monitor,
                "DB": db_sync,
                "MP": data_plan_migration,
                "RA": device_acl,
                "OA": device_acl,
            }

            MOD_KEYS = modules.keys()
            if action not in list(MOD_KEYS):
                log("Opcion No valida", "fail")
                sleep(2)
                return

            devices = olt_devices if action not in ["MR", "RA"] else rtr_devices
            device = (
                inp("Seleccione la OLT a usar [1 | 2 | 3] : ")
                if action not in ["MR", "RA"]
                else inp("Selecciona el router a monitorear [E1 | E2 | A1 | A2] : ")
            )
            debug = bool(inp("Enable debug [mostrar comandos]? (y/n): ").strip() == "Y")
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
