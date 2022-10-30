import pandas as pd


def parserCSV(path):
    file = pd.read_csv(path, encoding="latin1")
    data = file.to_dict("records")
    return data


def converter(path, filename, data, show):
    value = pd.DataFrame.from_records(data)
    if show:
        value.to_csv(f"{path}/{filename}.csv", index=None)
    else:
        value.to_csv(f"{filename}.csv", index=None)
