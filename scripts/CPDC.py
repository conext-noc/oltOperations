from tkinter import filedialog
from helpers.clientFinder.wan import wan
from helpers.fileFormatters.fileHandler import dictToFile
from helpers.fileFormatters.table import clientsTable
from helpers.info.regexConditions import ports
from helpers.utils.printer import colorFormatter, log


def cpdc(comm, command, quit, olt, action):
    """
    should return an xlsx with the corresponding client's data:
    FIRST_NAME + LAST_NAME + CONTRACT | SN | OLT | FRAME | SLOT | PORT | ONU ID | STATE | PLAN | SPID |

    map the plan and vlan to set the plan_name var

    as obj 
    {
      name,
      sn,
      olt,
      frame,
      slot,
      port,
      onu_id,
      state,
      plan_name,
      spid
    }
    """
    lst = ports["olt"][olt]
    clients = clientsTable(comm, command, lst)
    clientList = []
    print(f"the total # of clients @ port {clients[0]['frame']}/{clients[0]['slot']}/{clients[0]['port']} is : {len(clients)}")
    for client in clients:
        (_, WAN) = wan(comm,command,client['frame'], client['slot'],client['port'], client['onu_id'], olt)
        data = client.copy()
        print(f"{client['frame']}/{client['slot']}/{client['port']}/{client['onu_id']}")
        for idx,wanData in enumerate(WAN):
            data[f"vlan_{idx}"] = wanData['vlan']
            data[f"spid_{idx}"] = wanData['spid']
            data[f"plan_{idx}"] = wanData['plan']
            data[f"plan_name_{idx}"] = wanData['plan_name']
        clientList.append(data)
    path = filedialog.askdirectory()
    dictToFile(f"CPDC_{clients[0]['frame']}-{clients[0]['slot']}-{clients[0]['port']}", "E", path, clientList, True)
    log(colorFormatter("LISTA GENERADA SATISFACTORIAMENTE","success"))
    quit()