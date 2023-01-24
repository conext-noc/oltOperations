from helpers.fileFormatters.table import clientsTable
from helpers.info.regexConditions import ports


def cpdc(comm, command, quit, olt, action):
    """
    should return an xlsx with the corresponding client's data:
    FIRST_NAME + LAST_NAME + CONTRACT | SN | OLT | FRAME | SLOT | PORT | ONU ID | STATE | PLAN | SPID |

    map the plan and vlan to set the plan_name var

    as obj 
    {
      name,DONE
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
    """
    {
      'fsp': '#/#/###',
      'frame': #, 
      'slot': #,
      'port': #,
      'onu_id': #,
      'name': 'NAME',
      'status': 'online',
      'pwr': '-##.##',
      'state': 'STATE',
      'last_down_cause': 'CAUSE',
      'last_down_time': '##:##:##',
      'last_down_date': '####-##-##',
      'sn': 'SN_NUMBER',
      'device': 'DEVICE'
    }
    """
    for client in clients:
      print(client)
    quit()