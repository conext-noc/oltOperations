def compare(list1, list2):
    listData = []
    for item1 in list1:
        for item2 in list2:
            if (item1["ci"] == item2["ci"]):
                listData.append({"nombre": item1["nombre"], "frame": item2["f"],
                                "slot": item2["s"], "port": item2["p"], "id": item2["id"]})
    return listData
