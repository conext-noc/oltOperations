from helpers.info.plans import plans
from helpers.operations.spid import spidCalc
from helpers.utils.printer import colorFormatter, log

def addWanConfig(comm, command, quit, olt, lst):
    """
    lst should be formatted as the data object across the app
    {
      "fName",
      "lName",
      "nif",
      "contract",
      "olt",
      "frame",
      "slot",
      "port",
      "id",
      "sn",
      "plan",
    }
    """
    for client in lst:
        NAME = f'{client["fName"].upper()} {client["lName"].upper()} {client["contract"]}'
        command(f"interface gpon {client['frame']}/{client['slot']}")
        command(f"ont wan-config {client['port']} {client['id']} ip-index 2 profile-id 0")
        command("quit")
        resp = f"""
    | {NAME} {client["frame"]}/{client["slot"]}/{client["port"]}/{client["id"]}
    | {client["plan"]}
    Successfully Added Wan Profile @ ONT!
        """
        log(colorFormatter(resp,"success"))