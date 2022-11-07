import pandas as pd
from io import StringIO
import csv
import os


def fromCsvALT(path):
    with open(path) as f:
        reader = csv.DictReader(f)
        print(reader)
        return reader

def dictConverter(string):
    data = pd.read_csv(StringIO(string), sep=",").to_dict("records")
    return data


def fromCsv(path):
    file = pd.read_csv(path, encoding="latin1")
    data = file.to_dict("records")
    return data


def toCsv(path, filename, data, show):
    value = pd.DataFrame.from_records(data)
    if show:
        value.to_csv(f"{path}/{filename}.csv", index=None)
    else:
        value.to_csv(f"{filename}.csv", index=None)
