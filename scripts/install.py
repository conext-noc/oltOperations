from helpers.constants.definitions import InstallRequest, Onu, Zone, List, AvailableOnu
from helpers.constants.db_values import plan_list, onu_list
from helpers.handlers.smartolt import SmartOLT
from helpers.handlers.printer import log, inp


def onu_install(*, smart_olt_client: SmartOLT, **kwargs):
    all_available_onus: AvailableOnu = smart_olt_client.get_available_onus()
    sn_to_install = "HWTC" + inp(
        "Ingrese el serial del cliente a instalar [ultimos 8 digitos]  : "
    )
    log(
        value="| {:^3} | {:^7} | {:^16} | {:^12} |".format(
            "IDX", "F/S/P", "SN", "EQUIPO"
        )
    )
    selected_onu: AvailableOnu = AvailableOnu(frame=0, slot=0, port=0, olt=0, fsp="-", sn="-", device="-")
    onu_exists: bool = False
    for idx, available_onu in enumerate(all_available_onus):
        text = "| {:^3} | {:^7} | {:^16} | {:^12} |".format(
            idx, available_onu.fsp, available_onu.sn, available_onu.device
        )
        if available_onu.sn == sn_to_install:
            selected_onu = available_onu
            onu_exists = True
            log(value=text, variant="success")
        else:
            log(value=text)

    if not onu_exists:
        log(value="No se encontro ningun ONT con ese SN...", variant="warning")
        return

    device_info: List[Onu] = [onu for onu in onu_list if onu.device == selected_onu.device]
    if device_info is None or len(device_info) < 1:
        log(
            value=f"No se encontro ningun ONT con ese DEVICE_ID... DEVICE_ID:{selected_onu.device}",
            variant="warning",
        )
        return
    onu_device_info: Onu = device_info[0]
    name = inp("Ingrese el Nombre Completo del cliente separado por espacios : ")
    contract = inp("Ingrese el contrato del cliente : ").replace(" ", "").zfill(0)

    # looks up for all zones in system
    zones: List[Zone] = smart_olt_client.get_zones()
    log(value="| {:^3} | {:^16} |".format("IDX", "NOMBRE DE ZONA"))

    for idx, zone in enumerate(zones):
        log(value="| {:^3} | {:^16} |".format(idx, zone.name))

    selected_zone = None

    while selected_zone is None:
        try:
            selected_zone = int(inp("ingrese el indice de la zona del cliente   :   "))
            if selected_zone < 0 or selected_zone >= len(zones):
                log(value="Índice inválido. Por favor, inténtelo de nuevo.")
                selected_zone = None
        except ValueError:
            log(value="Entrada no válida. Por favor, ingrese un número.")

    # enter address
    onu_address = (
        inp("ingrese la direccion completa del cliente   :   ")
        .replace(" ", "_")
        .upper()
    )
    onu_lat = onu_address = float(
        inp("Ingrese la latitud del cliente   :   ") or 10.653860
    )
    onu_long = onu_address = float(
        inp("Ingrese la longitud del cliente   :   ") or -71.645966
    )

    # looks up for all obds in zone
    odbs = smart_olt_client.get_odbs(zone_id=zones[selected_zone].zone_id)
    odb = "CP1-FDT1-DB1-FAT1"  # default element value
    if len(odbs) > 0:
        log(value="| {:^3} | {:^24} |".format("IDX", "NOMBRE DE ELEMENTO"))
        for idx, odb in enumerate(odbs):
            log(value="| {:^3} | {:^24} |".format(idx, odb.name))
        selected_odb = inp(
            "ingrese el indice del elemento del cliente/Enter para saltar   :   "
        )
        odb = odbs[int(selected_odb) if selected_odb != "" else 0]

    # plan selection
    # from DB retrieve all plans
    log(value="| {:^3} | {:^16} |".format("IDX", "NOMBRE DE PLAN"))

    for idx, plan in enumerate(plan_list):
        log(value="| {:^3} | {:^16} |".format(idx, plan.name))

    selected_plan = None

    while selected_plan is None:
        try:
            selected_plan = int(inp("ingrese el indice del plan del cliente   :   ") or 0)
            if selected_plan < 0 or selected_plan >= len(plan_list):
                log(value="Índice inválido. Por favor, inténtelo de nuevo.")
                selected_plan = None
        except ValueError:
            log(value="Entrada no válida. Por favor, ingrese un número.")

    selected_profile = plan_list[selected_plan].profile
    onu_vlan = plan_list[selected_plan].vlan

    # state vals
    onu_temp = 25.0  # ssh in olt
    onu_power = 0.0  # ssh in olt

    onu_to_install: InstallRequest = InstallRequest(
        contract=contract,
        name=name,
        pon="gpon",
        olt=selected_onu.olt,
        sn=selected_onu.sn,
        frame=selected_onu.frame,
        slot=selected_onu.slot,
        port=selected_onu.port,
        device=onu_device_info.device,
        plan=selected_plan,
        profile=selected_profile,
        address=onu_address,
        vlan=onu_vlan,
        mode=onu_device_info.mode,
        temp=onu_temp,
        power=onu_power,
        fsp=selected_onu.fsp,
        zone=selected_zone,
        odb=odb,
        latitude=onu_lat,
        longitude=onu_long,
    )

    resp = smart_olt_client.onu_add(onu_data=onu_to_install)
    print(resp)
    # save in db
    
    print(onu_to_install)
