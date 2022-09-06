def compare(list1, list2):
    listData = []
    for item1 in list1:
        for item2 in list2:
            if (item1["Cliente/NIF"] == item2["Cliente/NIF"]):
                listData.append({"nombre": item1["Cliente"], "frame": item2["f"],
                                "slot": item2["s"], "port": item2["p"], "id": item2["id"], "ID externo": item1["ID externo"], "Cliente/NIF": item1["Cliente/NIF"]})
    return listData
