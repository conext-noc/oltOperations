import os
from dotenv import load_dotenv
from helpers.csvParser import parser
from activate.activate import activate
from helpers.listChecker import compare
from deactivate.deactivate import deactivate
# from helpers.verification import verify
load_dotenv()

username = os.environ["user"]
password = os.environ["password"]
port = os.environ["port"]


if __name__ == "__main__":
    delay = 2

    def main():
        action = input(
            "Which action will be performed? [activate | deactivate] : ")
        olt = input("In Which OLT the action will be performed? [1|2] : ")
        # actList = input("is a small lot? [yes | no] : ")
        ip = "181.232.180.5" if olt == "1" else "181.232.180.6"
        # list1 = parser("LISTAS/LISTA_DE_CORTE.csv")
        # list2 = parser("LISTAS/LISTA_DE_CLIENTES.csv")
        # actionList1 = compare(list1, list2)
        actionList = parser(
            "LISTAS/OLT1.csv") if olt == "1" else parser("LISTAS/OLT2.csv")
        # actionList = actionList2 if actList == "yes" else actionList1
        if (action == "activate"):
            activate(
                actionList, username, password, port, 1, ip)
            # verify(actionList, "{}ResultOLT.txt".format(action))
        if (action == "deactivate"):
            deactivate(
                actionList, username, password, port, 1, ip)
            # verify(actionList, "{}ResultOLT.txt".format(action))
        # return clients
    main()
