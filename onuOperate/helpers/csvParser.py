import csv


def parser(path):
    with open(path, "r", encoding="utf8") as f:
        data = list(csv.DictReader(f))
    return data
