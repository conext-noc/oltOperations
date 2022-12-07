from helpers.printer import colorFormatter, inp, log
from tkinter import filedialog
from helpers.fileHandler import dictToFile, fileToDict


def listCompare():
    fileType1 = inp("Es un archivo CSV o EXCEL? [C : E]: ")
    log("Selecciona la lista con datos de Odoo")
    fileName1 = filedialog.askopenfilename()
    odoo = fileToDict(fileName1, fileType1)

    fileType2 = inp("Es un archivo CSV o EXCEL? [C : E]: ")
    log("Selecciona la lista con datos CPDC")
    fileName2 = filedialog.askopenfilename()
    cpdc = fileToDict(fileName2, fileType2)

    data = []
    for odooClient in odoo:
        for cpdcClient in cpdc:
            if odooClient["NIF"] == cpdcClient["CI"]:
                data.append(
                    {
                      "ID externo": odooClient["ID externo"],
                      "NIF_CPDC": cpdcClient["CI"],
                      "NIF_ODOO": odooClient["NIF"],
                      "NOMBRE": odooClient["Cliente"],
                      "NOMBRE_CPDC": cpdcClient["NAME"],
                      "OLT":cpdcClient["OLT"],
                      "SN":cpdcClient["SN"],
                      "FRAME":cpdcClient["FRAME"],
                      "SLOT":cpdcClient["SLOT"],
                      "PORT":cpdcClient["PORT"],
                      "ID":cpdcClient["ID"],
                    })
    savePath = filedialog.askdirectory()
    dictToFile("RESULTADO_LISTA_DE_CORTE","E",savePath,data,True)