from time import sleep
import paramiko
from helpers.handlers.request import db_request
from helpers.handlers.printer import log, debug_log
from helpers.utils.decoder import decoder
from helpers.constants.definitions import endpoints


def ssh(ip, debugging):
    count = 0
    delay = 0.75
    conn = paramiko.SSHClient()
    conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    comm = None
    cont = True
    creds = db_request(endpoints["get_creds"], {})

    # Handling multiple SSH sessions
    while cont and count < len(creds["data"]):
        try:
            username = creds["data"][count]["user_name"]
            password = creds["data"][count]["password"]
            port = 22
            log(f"trying to connect with {username} @ {ip}", "info")
            conn.connect(ip, port, username, password, timeout=60)
            comm = conn.invoke_shell()
            cont = False
            break
        except Exception as e:
            log(f"failed to connect with {username} @ {ip} - Error: {e}", "info")
            cont = True
            count += 1
            if count < len(creds["data"]):
                log(f"retrying to re-connect with {creds['data'][count]['user_name']} @ {ip}", "info")
            else:
                log("No more credentials to try or connection refused. Exiting...", "fail")
                import sys
                sys.exit(1)
            continue

    def enter():
        comm.send(" \n")
        comm.send(" \n")
        sleep(delay)

    def command(cmd):
        comm.send(cmd)
        sleep(delay)
        debug_log(cmd)
        if debugging:
            log(
                f"""
{cmd}""",
                "info",
            )
        enter()

    def quit_ssh():
        conn.close()

    if ip in ["181.232.180.5", "181.232.180.6", "181.232.180.7"]:
        command("enable")
        command("config")
        command("scroll 512")
    else:
        command("\n")
        command("N")
        command("\n")
        command("sys")
    val = decoder(comm)
    # print(val)
    return (comm, command, quit_ssh)
