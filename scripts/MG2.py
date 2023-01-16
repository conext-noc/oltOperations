from tkinter.filedialog import askopenfilename
from helpers.utils.printer import colorFormatter, inp, log
from helpers.fileFormatters.fileHandler import fileToDict

def addWanConfig(comm, command, quit, olt, action):
    """"
    lst should be formatted as the data object across the app
    {
      "first_name",
      "last_name",
      "nif",
      "contract",
      "olt",
      "frame",
      "slot",
      "port",
      "onu_id",
      "sn",
      "plan_name",
    }
    """
    fileType = inp("Ingrese el tipo de archivo [E | C] : ")
    fileName = askopenfilename()
    lst = fileToDict(fileName,fileType)
    for client in lst:
        NAME = f'{client["first_name"].upper()} {client["last_name"].upper()} {client["contract"]}'
        command(f"interface gpon {client['frame']}/{client['slot']}")
        command(f"ont wan-config {client['port']} {client['onu_id']} ip-index 2 profile-id 0")
        command("quit")
        resp = f"""
    | {NAME} {client["frame"]}/{client["slot"]}/{client["port"]}/{client["onu_id"]}
    | {client["plan_name"]}
    Successfully Added Wan Profile @ ONT!
        """
        log(colorFormatter(resp,"success"))
    quit()
    return