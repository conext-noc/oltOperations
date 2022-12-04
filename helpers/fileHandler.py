import pandas as pd
from io import StringIO


def dictConverter(string):
    data = pd.read_csv(StringIO(string), sep=",").to_dict("records")
    return data


def fileToDict(fileName, fileType):
    file = pd.read_excel(fileName) if fileType == "E" else pd.read_csv(
        fileName, encoding='latin1')
    data = file.to_dict("records")
    return data


def dictToFile(fileName, fileType, path, data, show):
    value = pd.DataFrame.from_records(data)
    resPath = f"{path}/" if show else ""
    value.to_csv(f"{resPath}/{fileName}.csv",
                 index=None) if fileType == "C" else value.to_excel(f"{resPath}/{fileName}.xlsx")
