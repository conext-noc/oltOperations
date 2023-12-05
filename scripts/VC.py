from time import sleep
from helpers.handlers.fail import fail_checker
from helpers.handlers.wan_handler import wan_data
from helpers.utils.decoder import decoder, check, check_iter
from helpers.handlers.display import display
from helpers.handlers.printer import inp, log
from helpers.constants.regex_conditions import speed
from helpers.handlers.request import db_request
from helpers.constants.definitions import payload, endpoints
from helpers.finder.optical import optical_values
from helpers.finder.last_down_onu import down_values
from helpers.handlers.spid import calculate_spid


def client_traffic(comm, command, quit_ssh, device, _):
    speed_up_arr = []
    speed_down_arr = []
    payload["lookup_type"] = inp(
        "Buscar cliente por Contrato, Serial o Datos [C | S | D] : "
    )
    value = inp("Ingrese el contrato, serial o datos (f/s/p/id) : ")

    value = value.zfill(10) if payload["lookup_type"] == "C" else value
    value_class = (
        "contract"
        if payload["lookup_type"] == "C"
        else "fspi"
        if payload["lookup_type"] == "D"
        else "serial"
    )

    payload["lookup_value"] = {"olt": device, f"{value_class}": value}
    req = db_request(endpoints["get_client"], payload)
    if req["error"]:
        log(req["message"], "fail")
        quit_ssh()
        return
    client = req["data"]
    client["olt"] = device
    (client["temp"], client["pwr"], client["pwr_rx"]) = optical_values(comm, command, client, False)
    (
        client["last_down_cause"],
        client["last_down_time"],
        client["last_down_date"],
        client["status"],
    ) = down_values(comm, command, client, False)
    client["spid"] = calculate_spid(client)[
        "I" if "_IP" not in client["plan_name"] else "P"
    ]
    (client["ip"], client["mask"]) = wan_data(comm, command, client)
    proceed = display(client, "A")
    if not proceed:
        log("Cancelando...", "warning")
        quit_ssh()
        return
    command(f"interface gpon {client['frame']}/{client['slot']}")
    for i in range(0, 10):
        command(f"display ont traffic {client['port']} {client['onu_id']}")
        sleep(5)
        output_speed = decoder(comm)
        fail = fail_checker(output_speed)
        if fail is None:
            (_, s_up_speed) = check(output_speed, speed["up"]).span()
            (e_up_speed, s_down_speed) = check(output_speed, speed["down"]).span()
            (e_down_speed, _) = check_iter(output_speed, speed["cond"])[2]
            up_speed = int(output_speed[s_up_speed:e_up_speed])
            down_speed = int(output_speed[s_down_speed:e_down_speed])
            speed_up_arr.append(up_speed)
            speed_down_arr.append(down_speed)
        else:
            speed_up_arr.append(0)
            speed_down_arr.append(0)
        i = i + 1
    command("quit")
    up_len = len(speed_up_arr)
    up_sum = sum(speed_up_arr)
    up_avg = up_sum / up_len
    down_len = len(speed_down_arr)
    down_sum = sum(speed_down_arr)
    down_avg = down_sum / down_len
    log(
        f"""
El consumo promedio del ONT es {up_avg} Kbps [UP] y {down_avg} Kbps [DOWN]
""",
        "info",
    )
    quit_ssh()
