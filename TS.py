# from time import sleep
# from tkinter.filedialog import askopenfilename
# from helpers.fileFormatters.fileHandler import fileToDict
# from helpers.utils.decoder import decoder
# from helpers.utils.printer import inp
# from helpers.utils.ssh import ssh

# def device_config():
#     ip = input("IP of device : ")
#     (comm, command, quit) = ssh(ip)
#     command("dis cu | n")
#     sleep(10)
#     output = decoder(comm)
#     device_name = input("Device name : ")
#     print(output, file=open(f"{device_name}.txt", "a"))
#     quit()
# # device_config()

# def excelTester():
#     fileType = inp("Ingrese el tipo de archivo [E | C] : ")
#     fileName = askopenfilename()
#     lst = fileToDict(fileName, fileType)
#     for client in lst:
#         print(client)
# # excelTester()


import enum
from time import sleep
from helpers.failHandler.fail import failChecker
from helpers.fileFormatters.fileHandler import dataToDict
from helpers.utils.decoder import checkIter, decoder
from helpers.utils.printer import inp
from helpers.utils.ssh import ssh

infoHeader = "NA,F/,S/P,ID,SN,control_flag,run_state,config_state,match_state,protect_side,NA"
descHeader = "NA,F/,S/P,ID,NAME1,NAME2,NAME3,NAME4,NAME5,NAME6,NAME7,NA"

condition = "-----------------------------------------------------------------------------"
newCond = "----------------------------------------------------------------------------"
newCondFSP = "F/S/P               : "
newCondSn = "Ont SN              : "
newCondTime = "Ont autofind time   : "

####################             IN MAINTANCE             ####################


def nameLookup():
    ip = "181.232.180.7"
    debug = True
    (comm, command, quit) = ssh(ip, debug)
    decoder(comm)
    clients = []
    # NAME = inp("Ingrese el Nombre del Cliente a buscar : ")
    NAME = "MARIA"
    command(f'display ont info by-desc "{NAME}" | no-more ')
    sleep(5)
    value = decoder(comm)
    regex = checkIter(value, condition)
    FAIL = failChecker(value)
    portRange = []
    if FAIL == None:
        ttlPorts = len(regex) // 6
        print(len(regex))
        for i in range(len(regex)):
            # if idx % 2 != 0:
            #     continue
            print(value[regex[i][1] + 1:regex[i+1][0] - 1])

            # portRange.append({"sInfo": regex[port+1][1], "eInfo": regex[port + 2]
            #                  [0], "sDesc": regex[port + 3][1], "eDesc": regex[port + 4][0]})
        # for i in range(0, ttlPorts):
        #     print("info", value[portRange[i]["sInfo"]:portRange[i]["eInfo"]])
        #     print("desc", value[portRange[i]["sDesc"]:portRange[i]["eDesc"]])
        ############         ^  SO FAR SO GOOD ^             ###############
     #    for info in portRange:
     #        valueInfo = dataToDict(
     #            infoHeader, value[info["sInfo"]:info["eInfo"]])
     #        valueDesc = dataToDict(
     #            descHeader, value[info["sDesc"]:info["eDesc"]])
     #        for (info, desc) in zip(valueInfo, valueDesc):
     #            if info["ID"] == desc["ID"]:
     #                name = ""
     #                SLOT = int(desc["S/P"].split("/")[0])
     #                PORT = int(desc["S/P"].split("/")[1])
     #                for i in range(1, 7):
     #                    NAME = str(desc[f"NAME{i}"]) if str(
     #                        desc[f"NAME{i}"]) != "nan" else ""
     #                    name += NAME + " "
     #                clients.append({
     #                    "frame": 0,
     #                    "slot": SLOT,
     #                    "port": PORT,
     #                    "id": desc["ID"],
     #                    "name": name,
     #                    "state": info["control_flag"],
     #                    "status": info["run_state"],
     #                    "sn": info["SN"]
     #                })
     #    return {
     #        "data":clients,
     #        "fail": FAIL
     #    }
    quit()


#    return {
#            "data":clients,
#            "fail": FAIL
#        }
nameLookup()

####################             IN MAINTANCE             ####################
