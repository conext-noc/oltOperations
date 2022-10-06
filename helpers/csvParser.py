import csv

def parser(path):
    with open(path, "r", encoding="utf8") as f:
        data = list(csv.DictReader(f))
    return data

def converter(path,filename,data,show):
    keys = data[0].keys()
    if(show):
        with open(f'{path}/{filename}.csv', 'w', newline='') as f:
            dict_writer = csv.DictWriter(f, keys)
            dict_writer.writeheader()
            dict_writer.writerows(data)
    else:
        with open(f'{filename}.csv', 'w', newline='') as f:
            dict_writer = csv.DictWriter(f, keys)
            dict_writer.writeheader()
            dict_writer.writerows(data)
