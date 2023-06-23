import re
from time import sleep
from helpers.utils.decoder import decoder, check_iter
from helpers.handlers import (
    printer,
    fail as FAIL,
    file_formatter,
)
from helpers.constants import regex_conditions


log = printer.log
data_to_dict = file_formatter.data_to_dict
port_summary = regex_conditions.port_summary
condition_port_summary = regex_conditions.condition_port_summary
fail_checker = FAIL.fail_checker


def clients_table(comm, command, lst):
    clients = []
    for idx, lt in enumerate(lst):
        fsp = lt["fsp"]
        FRAME = int(fsp.split("/")[0])
        SLOT = int(fsp.split("/")[1])
        PORT = int(fsp.split("/")[2])
        command(f"display ont info summary {fsp} | no-more")
        sleep(2.5)
        value = decoder(comm)
        fail = fail_checker(value)
        if fail is None:
            states_summary = []
            names_summary = []
            re_summ = check_iter(value, condition_port_summary)
            for op in port_summary:
                name = op["name"]
                start = op["start"]
                end = op["end"]
                header = op["header"]
                (_, s) = re_summ[start]
                (e, _) = re_summ[end]
                if name == "names":
                    names_summary = data_to_dict(header, value[s:e])
                else:
                    states_summary = data_to_dict(header, value[s:e])

            for status, names in zip(states_summary, names_summary):
                if int(status["onu_id"]) == int(names["onu_id"]):
                    name = ""
                    for i in range(1, 4):
                        name += str(names[f"name{i}"]) + " "
                    clients.append(
                        {
                            "fsp": fsp,
                            "fspi": f'{fsp}/{status["onu_id"]}',
                            "frame": FRAME,
                            "slot": SLOT,
                            "port": PORT,
                            "onu_id": status["onu_id"],
                            "name": re.sub(" +", " ", name).replace("\n", "").strip(),
                            "status": status["state"],
                            "last_down_time": status["down_time"],
                            "pwr": names["rx_tx_power"].split("/")[0],
                            "last_down_date": status["down_date"],
                            "last_down_cause": status["down_cause_1"],
                            "sn": names["sn"],
                            "device": names["device"],
                        }
                    )

            log(f"{idx} {fsp} done", "ok")
        else:
            log(fail, "fail")
            continue
    return clients
