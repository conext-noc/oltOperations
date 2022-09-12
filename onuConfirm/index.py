from dotenv import load_dotenv
import os
import paramiko
from spidInfo import getSPID
from onuIdInfo import addONU,addOnuService
from ontCheck import verifyValues
load_dotenv()

username = os.environ["user"]
password = os.environ["password"]
port = os.environ["port"]

providerMap = {
  "inter": 1101,
  "vnet": 1102
}

conditionTemp = "Temperature\(C\)                         : "
conditionPwr = "Rx optical power(dBm)                  : "


if __name__ == "__main__":
  def main():
    delay = 1
    olt = input("Select OLT [1|2] :")
    ip = "181.232.180.5" if olt == "1" else "181.232.180.6"
    isNew = input("will you add a new client? [y|n]")
    if(isNew == "y"):
      clientSlot = input("enter client slot : ")
      clientPort = input("enter client port : ")
      clientName = input("enter the ont client name : ")
      clientProvider = input("enter client Provider [inter | vnet] : ")
      clientSN = input("enter client serial : ")
      clientPlan = input("enter the client's data plan : ")
      deviceType = input("enter the client ONU type : ")
      conn = paramiko.SSHClient()
      conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
      conn.connect(ip, port, username, password)
      comm = conn.invoke_shell()

      spid = getSPID(comm,delay)
      ontId = addONU(comm,clientSN,clientSlot,clientPort,clientProvider,clientName,delay,deviceType)
      (temp,pwr) = verifyValues(comm,clientSlot,clientPort,ontId,delay)
      proceed = input(f"ONT power is {pwr} and Temperature is {temp} do you want to proceed? [y|n] : ")
      if(proceed == "y"):
        addOnuService(comm,delay,spid,clientProvider,clientSlot,clientPort,ontId,clientPlan)
        print(f"""
        {clientName} 0/{clientSlot}/{clientPort}/{ontId} OLT {olt} {clientPlan[3:]}
        TEMPERATURA: {temp}
        POTENCIA: {pwr}
        """)
        os.remove("ResultSPID.txt")
        os.remove("ResultONTID.txt")
        os.remove("ResultPwr.txt")
        os.remove("ResultTemp.txt")
        conn.close()
        return
      if(proceed == "n"):
        reason = input("why the ont wont have service? : ")
        print(f"""
        {clientName} 0/{clientSlot}/{clientPort}/{ontId} OLT {olt} {clientPlan[3:]}
        TEMPERATURA: --
        POTENCIA: --
        - {reason} -
        SPID : {spid}
        """)
        os.remove("ResultSPID.txt")
        os.remove("ResultONTID.txt")
        os.remove("ResultPwr.txt")
        os.remove("ResultTemp.txt")
        conn.close()
        return
    if(isNew == "n"):
      conn = paramiko.SSHClient()
      conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
      conn.connect(ip, port, username, password)
      comm = conn.invoke_shell()

      spid = input("enter the corresponding service port virtual id")
      clientSlot = input("enter client slot : ")
      clientPort = input("enter client port : ")
      clientONUID = input("enter client onu id : ")
      clientName = input("enter client name : ")
      clientProvider = input("enter client Provider [inter | vnet] : ")
      clientPlan = input("enter the client's data plan : ")
      
      (temp,pwr) = verifyValues(comm,clientSlot,clientPort,clientONUID,delay)
      proceed = input(f"ONT power is {pwr} and Temperature is {temp} do you want to proceed? [y|n] : ")
      if(proceed == "y"):
        addOnuService(comm,delay,spid,clientProvider,clientSlot,clientPort,clientONUID ,clientPlan)
        print(f"""
        {clientName} 0/{clientSlot}/{clientPort}/{clientONUID} OLT {olt} {clientPlan[3:]}
        TEMPERATURA: {temp}
        POTENCIA: {pwr}
        """)
        os.remove("ResultSPID.txt")
        os.remove("ResultONTID.txt")
        os.remove("ResultPwr.txt")
        os.remove("ResultTemp.txt")
        conn.close()
        return
      if(proceed == "n"):
        reason = input("why the ont wont have service? : ")
        print(f"""
        {clientName} 0/{clientSlot}/{clientPort}/{ontId} OLT {olt} {clientPlan[3:]}
        TEMPERATURA: --
        POTENCIA: --
        - {reason} -
        SPID : {spid}
        """)
        os.remove("ResultSPID.txt")
        os.remove("ResultONTID.txt")
        os.remove("ResultPwr.txt")
        os.remove("ResultTemp.txt")
        conn.close()
        return

  main()


