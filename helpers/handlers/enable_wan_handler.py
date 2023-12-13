
from helpers.handlers.printer import inp


def enable_wan(command, client):
    enable = inp("Desea habilitar el puerto wan? [y/N] : ")
    if "Y" == enable:
        command("diagnose")
        command(f"ont wan-access http {client['frame']}/{client['slot']}/{client['port']} {client['onu_id']} enable")
