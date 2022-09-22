from onuOperate.operate import operate
from onuConfirm.confirm import confirm

if __name__ == "__main__":
    def main():
        while True:
            action = input(
                "que accion se realizara? [ activar/desactivar cliente (o) | agregar cliente (c) ] : ")
            if (action == "o"):
                operate()
            if (action == "c"):
                confirm()
    main()
