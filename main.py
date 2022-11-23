from helpers.formatter import colorFormatter
from time import sleep
import tkinter as tk
import traceback
from scripts.OLT import olt
from scripts.RTR import rtr

root = tk.Tk()
root.withdraw()


def main():
    try:
        while True:
            device = input(
                "Seleccione el equipo a utilizar [ROUTER | OLT] : ").upper()
            if device == "OLT":
                olt()
            elif device == "ROUTER":
                rtr()
            else:
              resp = colorFormatter(
                f"Error @ : opcion {device} no existe", "warning")
              print(resp)
              sleep(0.5)

    except KeyboardInterrupt:
        resp = colorFormatter("Saliendo...", "warning")
        print(resp)
        sleep(0.5)
    except Exception:
        resp = colorFormatter(f"Error At : {traceback.format_exc()}", "fail")
        print(resp)
        sleep(10)


if __name__ == "__main__":
    main()
