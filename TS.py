from time import sleep
from tkinter.filedialog import askopenfilename
from helpers.fileFormatters.fileHandler import fileToDict
from helpers.utils.decoder import decoder
from helpers.utils.printer import inp
from helpers.utils.ssh import ssh

def device_config():
    ip = input("IP of device : ")
    (comm, command, quit) = ssh(ip)
    command("dis cu | n")
    sleep(10)
    output = decoder(comm)
    device_name = input("Device name : ")
    print(output, file=open(f"{device_name}.txt", "a"))
    quit()
# device_config()

def excelTester():
    fileType = inp("Ingrese el tipo de archivo [E | C] : ")
    fileName = askopenfilename()
    lst = fileToDict(fileName, fileType)
    for client in lst:
        print(client)
excelTester()