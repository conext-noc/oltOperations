import os
from dotenv import load_dotenv
from csvParser import parser
from activate import activate
from listChecker import compare
from deactivate import deactivate
from verification import verify
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
        ip = "181.232.180.5" if olt == "1" else "181.232.180.6"
        list1 = parser("LISTAS/LISTA_DE_CORTE.csv")
        list2 = parser("LISTAS/LISTA_DE_CLIENTES.csv")
        actionList = compare(list1, list2)
        if (action == "activate"):
            activate(
                actionList, username, password, port, 1, ip)
            # verify(actionList, "{}ResultOLT.txt".format(action))
        if (action == "deactivate"):
            deactivate(
                actionList, username, password, port, 1, ip)
            # verify(actionList, "{}ResultOLT.txt".format(action))
        else:
            print("no")
        # return clients
    main()
