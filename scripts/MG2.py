from tkinter.filedialog import askopenfilename
from helpers.utils.printer import colorFormatter, inp, log
from helpers.fileFormatters.fileHandler import fileToDict

def addWanConfig(comm, command, quit, olt, action):
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
    fileType = inp("Ingrese el tipo de archivo [E | C] : ")
    fileName = askopenfilename()
    lst = fileToDict(fileName,fileType)
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
    quit()
    return