from helpers.info.plans import plans


def migration(comm, command, quit, olt, lst):
    """
    lst should be formatted as the data object across the app
    {
      "fName"
      "lName"
      "nif"
      "contract"
      "olt"
      "frame"
      "slot"
      "port"
      "id"
      "sn"
      "plan"
    }
    """
    for client in lst:
        command(f"interface gpon {client['frame']}/{client['slot']}")
        command(f'ont add {client["port"]} {client["id"]} sn-auth {client["sn"]} omci ont-lineprofile-id {plans[client["plan"]]["lineProfile"]} ont-srvprofile-id {plans[client["plan"]]["srvProfile"]} desc "{client["fName"].upper()} {client["lName"].upper()} {client["contract"]}" ')
