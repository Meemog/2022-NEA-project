def LinearSearch(itemSought, list):
    i = 0
    while i < len(list):
        if list[i] == itemSought:
            return i
    return None