def finder(lst, key, value):
    r = list(filter(lambda lt: lt[key] == value, lst))[0]
    for i, dic in enumerate(lst):
        if dic[key] == value:
            return (i,r)
    return (-1, None)
