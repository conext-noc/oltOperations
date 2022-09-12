from onuOperate.operate import operate
from onuConfirm.confirm import confirm

if __name__ == "__main__":
    def main():
        action = input(
            "What will you do? [ activate/deactivate (o) | confirm/add (c) ] : ")
        if (action == "o"):
            operate()
        if (action == "c"):
            confirm()
    main()
